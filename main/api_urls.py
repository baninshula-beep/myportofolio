"""Education API routes, included beneath the project's ``/api/v1/`` prefix."""

from django.urls import path

from main.api_views import (
    education_detail,
    education_list_create,
    education_star,
)


urlpatterns = [
    path(
        "education/",
        education_list_create,
        name="api_education_list_create",
    ),
    path(
        "education/<int:education_id>/",
        education_detail,
        name="api_education_detail",
    ),
    path(
        "education/<int:education_id>/star/",
        education_star,
        name="api_education_star",
    ),
]
