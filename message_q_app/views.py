from django.http import JsonResponse
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import UsageKey
from lms.djangoapps.courseware.models import StudentModule
import traceback
import redis
import json
from celery import shared_task
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from lms.djangoapps.grades.tasks import recalculate_subsection_grade_v3
from lms.djangoapps.grades.tasks import ScoreDatabaseTableEnum
from opaque_keys.edx.locations import CourseLocator
import uuid

redis_client = redis.StrictRedis(host='host.docker.internal', port=6379, db=0, decode_responses=True)

@shared_task(queue="edx.lms.core.default")
def test_view(message_queue):
    print("test_view called")
    try:
        payload = message_queue 
        submission_id = payload.get('x-submission-id')
        redis_data = redis_client.hgetall(submission_id)
        if redis_data:
            #getting the usage_key and student_id from redis
            usage_key_from_redis = redis_data.get("usage_key")
            student_id_from_redis = redis_data.get("student_id")

            usage_key = UsageKey.from_string(usage_key_from_redis)
            
            #for xblock scope type content 
            xblock_instance = modulestore().get_item(usage_key)
            course_id = xblock_instance.course_id
            
            #for xblock user specific details
            score = payload.get('score')
            is_correct = payload.get('is_correct')
            message = payload.get('message')
            
            # #student module
            student_module = StudentModule.objects.get(student_id=student_id_from_redis, module_state_key=usage_key)
            state = json.loads(student_module.state)
            state['score'] = score
            state['message'] = message
            state['is_correct'] = is_correct
            student_module.state = json.dumps(state)
            student_module.save()

            #add or update grades for student
            student_module, created = StudentModule.objects.update_or_create(
            student_id = int(student_id_from_redis),
            module_state_key=str(usage_key),  
            defaults={
                "grade": payload.get("score"),           
                "max_grade": payload.get("maxscore")   , 
                "modified": timezone.now()
            }
            )

            #get the modified time
            modified_time = StudentModule.objects.filter(
                student_id = int(student_id_from_redis),
                course_id = course_id,
                module_state_key = str(usage_key)  
            ).values_list("modified", flat=True).first()    
            
            if modified_time:
                expected_timestamp = modified_time.timestamp()
                print("inside modified time")  
                #if modified time is there we are calling recalcuate
                if isinstance(course_id, CourseLocator):
                    course_id = str(course_id)
                recalculate_subsection_grade_v3(
                    user_id = int(student_id_from_redis),
                    course_id = course_id,
                    usage_id = str(usage_key),
                    only_if_higher=False,
                    event_transaction_id=str(uuid.uuid4()),
                    score_db_table=ScoreDatabaseTableEnum.courseware_student_module,
                    expected_modified_time=expected_timestamp,
                    score_deleted=False
                )
    except Exception as e:
        print( type(e), e)
        traceback.print_exc()


def for_api(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        submission_id = data.get('x-submission-id')
        redis_data = redis_client.hgetall(submission_id)
        if redis_data:
            #redis related
            usage_key_from_redis = redis_data.get("usage_key")
            student_id_from_redis = redis_data.get("student_id")

            block_usage_key = UsageKey.from_string(usage_key_from_redis)
            
            #add or update grades for student
            student_module, created = StudentModule.objects.update_or_create(
            student_id = int(student_id_from_redis),
            module_state_key=str(block_usage_key),  
            defaults={
                "grade": data.get("score"),           
                "max_grade": data.get("maxscore")   , 
                "modified": timezone.now()
            }
            )
            
            #module store
            xblock_instance = modulestore().get_item(block_usage_key)
            course_id = xblock_instance.course_id
            print(course_id, " course id#################################################")
            #fetching the modified time from student module
            modified_time = StudentModule.objects.filter(
                student_id = int(student_id_from_redis),
                course_id = course_id,
                module_state_key = str(block_usage_key)  
            ).values_list("modified", flat=True).first()    
                
            if modified_time:
                expected_timestamp = modified_time.timestamp()
                print("inside modified time")  
                #if modified time is there we are calling recalcuate
                if isinstance(course_id, CourseLocator):
                    course_id = str(course_id)
                recalculate_subsection_grade_v3(
                    user_id = int(student_id_from_redis),
                    course_id = course_id,
                    usage_id = str(block_usage_key),
                    only_if_higher=False,
                    event_transaction_id=str(uuid.uuid4()),
                    score_db_table=ScoreDatabaseTableEnum.courseware_student_module,
                    expected_modified_time=expected_timestamp,
                    score_deleted=False
                )
            
            print(student_module, " this is student module@@@#################")
            print(created, " this tell us that created or not@@#######################")
            return JsonResponse({'message': 'success'}, status = 200)
        return JsonResponse({'message': 'submission id missing in redis'}, status = 404)
    except json.JSONDecodeError:
        return JsonResponse({'message' : 'Invalid json'}, status = 400)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status = 500)
    