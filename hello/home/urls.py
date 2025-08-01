from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('',views.postblogs , name="home"),
    path('display',views.displayblogs , name="about"),
]