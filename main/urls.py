from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_education,
    create_education,
    update_education,
    get_education_json,
    delete_education,
)


app_name = "main"


urlpatterns = [
    path("", show_main, name="show_main"),

    path(
        "experience/",
        show_experience,
        name="show_experience"
    ),

    path(
        "education/",
        show_education,
        name="show_education"
    ),

    path(
        "education/add/",
        create_education,
        name="create_education"
    ),

    # Endpoint untuk mengambil data Education dalam format JSON.
    path(
        "api/education/",
        get_education_json,
        name="get_education_json"
    ),

    path(
        "education/<int:education_id>/delete/",
        delete_education,
        name="delete_education"
    ),

    path(
    "education/<int:education_id>/edit/",
    update_education,
    name="update_education"
    ),
]