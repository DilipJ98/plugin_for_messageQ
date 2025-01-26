"""
URLs for message_q_app.
"""
from django.urls import path 
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="message_q_app/base.html")),
]
