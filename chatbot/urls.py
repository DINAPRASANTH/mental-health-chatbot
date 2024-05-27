from django.urls import path
from . import views
from .views import preference_view
from .views import games_view

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('accounts/login/', views.login, name='login'),
    path('delete-chats/', views.delete_chats, name='delete_chats'),
    path('audio_chat/', views.audio_chat, name='audio_chat'),
    path('audio/', views.audio, name='audio'),
    path('preference/', preference_view, name='prefer'),
    path('games/', games_view, name='games'),
    path('videochat/', views.videochat, name='videochat'),
]
