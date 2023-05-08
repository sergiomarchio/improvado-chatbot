from django.urls import path

from . import views

app_name = 'chatbot'
urlpatterns = [
    path('', views.chat, name='chat'),
    path('clear/', views.clear, name='clear'),
    path('process_message/', views.process_message, name='process_message'),
]
