# message_q_app/api/urls.py
from django.urls import path
from ..views import test_view

app_name = 'message_q_app'  # This should match PluginURLs.APP_NAME

urlpatterns = [
    path('test/', test_view, name='test'),
]
