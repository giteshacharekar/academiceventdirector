from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
     path('postComment', views.postComment, name="postComment"),
    path('', views.eventHome, name="eventhome"),
    path('<str:slug>', views.eventPost, name="eventPost"),
    path('CreateNewPost', views.CreateNewPost, name='createpost'),
]