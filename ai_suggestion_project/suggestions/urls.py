from django.contrib import admin
from django.urls import path
from .views import GenerateSuggestionsAPIView

urlpatterns = [
    path("generate/", GenerateSuggestionsAPIView.as_view(), name="suggestions"),
]
