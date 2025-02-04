from django.http import JsonResponse
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import UsageKey
from lms.djangoapps.courseware.models import StudentModule
from lms.djangoapps.courseware.user_state_client import XBlockUserStateClient


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
            
            #xblockuser state client
            state_client = XBlockUserStateClient()
            print("state client object created.............")
            existing_state = state_client.get(student_id_from_redis, usage_key) or {}
            print(existing_state, " existing state from xblockuserstateclient from views####")
            if not existing_state:
                print("No existing state found, creating a new one.")
                existing_state = {"score": 0, "is_correct": False, "message": ""}
            existing_state["score"] = score
            existing_state["is_correct"] = is_correct
            existing_state["message"] = message
            print("daat assigned to existing state............")
            state_client.set(student_id_from_redis, usage_key, existing_state)
            print("data saved in xblockuserstateclient")

            #retrieve data from xblockuserstateclient
            user_state = state_client.get(student_id_from_redis, usage_key)
            print("data retrieved from xblockuserstateclient")
            print(user_state.get('score'), user_state.get('is_correct'), user_state.get('message'), " user state from xblockuserstateclient from views####")


            # #student module
            # student_module = StudentModule.objects.get(student_id=student_id_from_redis, module_state_key=usage_key)
            # state = json.loads(student_module.state)
            # state['score'] = score
            # state['message'] = message
            # student_module.state = json.dumps(state)
            # student_module.save()
            # print("data saved in student module")

            # #get updated values
            # updated_student_module = StudentModule.objects.get(student_id=student_id_from_redis, module_state_key=usage_key)
            # updated_state = json.loads(updated_student_module.state)
            # print(updated_state.get('score'), updated_state.get('message'), " updated state from student module")
            
            # results = xblock_instance.update_grades_of_student(student_id_from_redis, usage_key)
            # print(results, " resulsts from update fun ##############################")
            
            # print("try executing after update method in try")
    except Exception as e:
        print(e, "  something is woring in the catch block so exec block is executing..................################################3")
        return JsonResponse({'message': f"Error while updating item: {e}"})
    return JsonResponse({'message': "api working"})
