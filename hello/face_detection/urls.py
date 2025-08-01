from django.contrib import admin
from django.urls import path ,include
from face_detection import views

urlpatterns = [
    path("",views.index , name="home"),
    path("video_feed/", views.video_feed, name="video_feed"),
    path("run-start/",views.start_camera , name="start"),
    path("run-stop/",views.stop_camera , name="stop"),
    path("run-test/",views.start_testing , name="test"),
    path("run-train/",views.train_model_view , name="train"),
    path("run-stop_test/" , views.stop_testing , name="stoptest"),
    path("run-view_res/" , views.get_results , name="viewres")

]
