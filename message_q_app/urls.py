from django.urls import path
from .views import update_student_grade_view
from django.views.generic import TemplateView


app_name = 'message_q_app'

urlpatterns = [
    path('test/', update_student_grade_view, name='test'),
    path('home', TemplateView.as_view(template_name="message_q_app/base.html"), name='index'),
]



