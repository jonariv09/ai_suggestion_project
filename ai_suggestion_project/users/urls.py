from django.contrib import admin
from django.urls import path
from .views import RegistrationAPIView

urlpatterns = [
    path("", RegistrationAPIView.as_view(), name="users"),
]
