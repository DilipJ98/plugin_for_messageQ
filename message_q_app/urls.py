from django.urls import path
from .views import test_view, for_api
from django.views.generic import TemplateView


app_name = 'message_q_app'

urlpatterns = [
    path('test/', test_view, name='test'),
    path('test2/', for_api, name='test2') , 
    path('home', TemplateView.as_view(template_name="message_q_app/base.html"), name='index'),
]



