from django.urls import path
from hhh import views

urlpatterns = [
    path("", views.upload_image, name="home"),
]