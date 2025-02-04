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



def test_view(request):
    try:
        body = json.loads(request.body)
        submission_id = body.get('x-submission-id')
        redis_data = redis_client.hgetall(submission_id)
        print("inside try before redis")
        if redis_data:
            print("inside try after redis")
            usage_key_from_redis = redis_data.get("usage_key")
            student_id_from_redis = redis_data.get("student_id")
            location = "block-v1:cklabs+XBLOCK002+202_T1+type@textxblock+block@"+usage_key_from_redis
            usage_key = UsageKey.from_string(location)
            print(f"Usage Key from Redis: {usage_key_from_redis}")
            print(f"Student ID from Redis: {student_id_from_redis}")
            print(f"usage key: {usage_key}")
            xblock_instance = modulestore().get_item(usage_key)
            xblock_instance.marks = 10
            xblock_instance.boilerplate_code = "boilerplate code"
            score = body.get('score')
            is_correct = body.get('is_correct')
            message = body.get('message')

            modulestore().update_item(xblock_instance, student_id_from_redis)
            print("data saved in modulestore")
            
            # #student module
            student_module = StudentModule.objects.get(student_id=student_id_from_redis, module_state_key=usage_key)
            state = json.loads(student_module.state)
            state['score'] = score
            state['message'] = message
            state['is_correct'] = is_correct
            student_module.state = json.dumps(state)
            student_module.save()
            print("data saved in student module")

    except Exception as e:
        print( type(e), e)
        traceback.print_exc()
        return JsonResponse({'message': f"Error while updating item: {e}"})
    return JsonResponse({'message': "api working"})


@shared_task
def listen(data):
    print("Hurray inside listen###########")
    print(data, " data from messageQ")
    return data