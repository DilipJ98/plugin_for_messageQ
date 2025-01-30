from django.http import JsonResponse
from xblock.core import XBlock
from xblock.runtime import Runtime



def test_view(request):

    usage_key = "e34b28140bb048a7aa6eac8d0f13e6a9"
    runtime = Runtime()
    xblock_instance = runtime.get_block(usage_key)
    print(xblock_instance, " this is xblock instance..............1.................1111!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    return JsonResponse({'message': xblock_instance})
