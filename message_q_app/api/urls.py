from django.urls import path
from views import test_view

app_name = 'message_q_app'  # Should match PluginURLs.APP_NAME

urlpatterns = [
    path('test/', test_view, name='test'),
]
