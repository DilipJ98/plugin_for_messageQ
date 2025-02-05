from django.http import JsonResponse
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import UsageKey
from lms.djangoapps.courseware.models import StudentModule
# from lms.djangoapps.courseware.user_state_client import XBlockUserStateClient
import traceback

import redis
import json
from celery import shared_task

redis_client = redis.StrictRedis(host='host.docker.internal', port=6379, db=0, decode_responses=True)

@shared_task(queue="edx.lms.core.default")
def test_view(message):
    print("test_view called..###!!@@@#####@@@@@$$$$$$$$$")
    try:
        submission_id = message.get('x-submission-id')
        redis_data = redis_client.hgetall(submission_id)
        if redis_data:
            #getting the usage_key and student_id from redis
            usage_key_from_redis = redis_data.get("usage_key")
            student_id_from_redis = redis_data.get("student_id")
            location = "block-v1:cklabs+XBLOCK002+202_T1+type@textxblock+block@"+usage_key_from_redis
            usage_key = UsageKey.from_string(location)
            
            #for xblock scop type content 
            xblock_instance = modulestore().get_item(usage_key)
            xblock_instance.marks = 10
            xblock_instance.boilerplate_code = "boilerplate code"
            modulestore().update_item(xblock_instance, student_id_from_redis)
            
            #for xblock user specific details
            score = message.get('score')
            is_correct = message.get('is_correct')
            message = message.get('message')

            # #student module
            student_module = StudentModule.objects.get(student_id=student_id_from_redis, module_state_key=usage_key)
            state = json.loads(student_module.state)
            state['score'] = score
            state['message'] = message
            state['is_correct'] = is_correct
            student_module.state = json.dumps(state)
            student_module.save()

    except Exception as e:
        print( type(e), e)
        traceback.print_exc()
        return JsonResponse({'message': f"Error while updating item: {e}"})
    return JsonResponse({'message': "api working"})
