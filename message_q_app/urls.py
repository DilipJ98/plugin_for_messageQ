# """
# URLs for message_q_app.
# """
# from django.urls import path 
# from django.views.generic import TemplateView

# urlpatterns = [
#     path('', TemplateView.as_view(template_name="message_q_app/base.html")),
# ]

# message_q_app/urls.py
from django.urls import path, include
from django.views.generic import TemplateView


app_name = 'message_q_app'

urlpatterns = [

    # Non-API URLs
    path('', TemplateView.as_view(template_name="message_q_app/base.html"), name='index'),

    # Include the API URLs from api/urls.py
    path('api/', include('message_q_app.api.urls')),  # This will map /api/ to your API urls
]
