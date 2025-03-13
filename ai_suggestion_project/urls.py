from django.contrib import admin
from django.urls import path, include

API_PREFIX = "api"

urlpatterns = [
    path(
        f"{API_PREFIX}/users/",
        include(("ai_suggestion_project.users.urls", "users"), namespace="users"),
    ),
    path(
        f"{API_PREFIX}/suggestions/",
        include(("ai_suggestion_project.suggestions.urls", "suggestions"), namespace="suggestions"),
    ),
]
