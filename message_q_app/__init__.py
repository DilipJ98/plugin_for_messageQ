"""
This plugin is used to listen the message queue.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_q_app.settings')


__version__ = '0.1.0'

default_app_config = 'message_q_app.apps.MessageQAppConfig' 
# Expose key functions, views, etc.
from .views import test_view  # Expose test_view for direct import
from .urls import urlpatterns  # Expose urlpatterns if necessary

__all__ = ['test_view', 'urlpatterns']