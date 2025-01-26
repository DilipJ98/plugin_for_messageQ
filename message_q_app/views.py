from django.http import JsonResponse

def test_view(request):
    print('Message Queue App is working!............................................!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return JsonResponse({'message': 'Message Queue App is working!'})
