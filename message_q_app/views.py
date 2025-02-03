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
        print("inside try before redis")
        if redis_data:
            print("inside try after redis")
            usage_key_from_redis = redis_data.get("usage_key")
            student_id_from_redis = redis_data.get("student_id")
            location = "block-v1:cklabs+XBLOCK002+202_T1+type@textxblock+block@"+usage_key_from_redis
            usage_key = UsageKey.from_string(location)
            xblock_instance = modulestore().get_item(usage_key)
            xblock_instance.marks = 10
            xblock_instance.boilerplate_code = "boilerplate code"
            score = body.get('score')
            is_correct = body.get('is_correct')
            message = body.get('message')
            result = xblock_instance.update_grades_of_student(score, is_correct, message, student_id_from_redis)
            print(result, " this is result of update_grades_of_student method............................................")
            print("try executing after update method in try")
            # print(xblock_instance.runtime.get_runtime(), "this is runtime of xblock instance............................................")
            # runtime = xblock_instance.runtime
            # if runtime:
            #     print(runtime, "runtime is present")
            #     runtime.set_user_state(xblock_instance, {'score': body.get('score'), 'is_correct': body.get('is_correct'), 'message': body.get('message')}, user_id = student_id_from_redis)
            #     print("user details updated.....1.1.11.1.1.1..1.1.1.1#####################33")
            # else:
            #     print("runtime is not present")
            modulestore().update_item(xblock_instance, student_id_from_redis)
            print("try executing after update method in try")
    except Exception as e:
        print(e, "  something is woring in the catch block so exec block is executing..................################################3")
        return JsonResponse({'message': f"Error while updating item: {e}"})
    return JsonResponse({'message': "api working"})
