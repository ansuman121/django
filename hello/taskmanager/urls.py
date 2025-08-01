from django.contrib import admin
from django.urls import path ,include
from taskmanager import views
urlpatterns = [
    path("",views.view_task,name='home'),
    path("addtask" , views.add_task,name="add"),
    path("completetask/<int:id>/" ,views.completed_task,name="complete"),
    path("deletetask/<int:id>/" ,views.delete_task,name="delete")



]