from django.http import JsonResponse
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import UsageKey
import redis
import json


redis_client = redis.StrictRedis(host='host.docker.internal', port=6379, db=0, decode_responses=True)

def test_view(request):
    try:
        body = json.loads(request.body)
        submission_id = body.get('x-submission-id')
        redis_data = redis_client.hgetall(submission_id)
        if redis_data:
            usage_key_from_redis = redis_data.get("usage_key")
            student_id_from_redis = redis_data.get("student_id")

            location = "block-v1:cklabs+XBLOCK002+202_T1+type@textxblock+block@"+usage_key_from_redis
            usage_key = UsageKey.from_string(location)
            xblock_instance = modulestore().get_item(usage_key)
            xblock_instance.marks = 10
            xblock_instance.boilerplate_code = "boilerplate code"
            xblock_instance.score = body.get('score')
            xblock_instance.is_correct = body.get('is_correct')
            xblock_instance.message = body.get('message')

            modulestore().update_item(xblock_instance, student_id_from_redis)
            result = xblock_instance.update_grades_of_student()
            print(result, "this is result of grade funtion............................................")
            print("try executing after update method in try")
    except Exception as e:
        print(e)
        return JsonResponse({'message': f"Error while updating item: {e}"})
    return JsonResponse({'message': "api working"})
