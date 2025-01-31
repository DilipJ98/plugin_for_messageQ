from django.http import JsonResponse
from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import UsageKey

def test_view(request):
    location = "block-v1:cklabs+XBLOCK002+202_T1+type@textxblock+block@e34b28140bb048a7aa6eac8d0f13e6a9"
    usage_key = UsageKey.from_string(location)
    xblock_instance = modulestore().get_item(usage_key)
    print(xblock_instance.marks, "intial marks of the student")
    xblock_instance.marks = 3
    try:
        modulestore().update_item(xblock_instance, 8)
        print("try executing after update method in try")
    except Exception as e:
        print(e)
        return JsonResponse({'message': f"Error while updating item: {e}"})
    return JsonResponse({'message': "api working"})
