from django.urls import path
from main.api_views import (
    ExperienceDetailAPIView,
    ExperienceListCreateAPIView,
    ExperienceStarAPIView,
)

from main.views import (
    show_main,
    show_experience,
    get_experience_json,
    create_experience,
    update_experience,
    delete_experience,
    toggle_star,
    show_education,
    create_education,
    update_education,
    get_education_json,
    delete_education,
    register,
    login_user,
    logout_user,
    create_experience_ajax,
    create_education_ajax,
)


app_name = "main"


urlpatterns = [
    path(
        "",
        show_main,
        name="show_main"
    ),

    path(
        "register/",
        register,
        name="register"
    ),

    # =========================
    # EXPERIENCE
    # =========================

    path(
        "experience/",
        show_experience,
        name="show_experience"
    ),

    path(
        "experience/add/",
        create_experience,
        name="create_experience"
    ),

    path(
        "experience/add-ajax/",
        create_experience_ajax,
        name="create_experience_ajax"
    ),

    # Endpoint AJAX digunakan oleh frontend untuk menambah data
    # tanpa berpindah atau me-reload halaman.

    path(
        "experience/<uuid:experience_id>/edit/",
        update_experience,
        name="update_experience"
    ),

    path(
        "experience/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience"
    ),

    path(
        "experience/<uuid:experience_id>/star/",
        toggle_star,
        name="toggle_star"
    ),

    path(
        "experience/data/",
        get_experience_json,
        name="get_experience_json"
    ),

    # Endpoint JSON menyediakan data portfolio yang akan dirender
    # secara dinamis oleh JavaScript.

    path(
        "api/v1/experience/",
        ExperienceListCreateAPIView.as_view(),
        name="api_experience_list_create",
    ),

    path(
        "api/v1/experience/<uuid:id>/",
        ExperienceDetailAPIView.as_view(),
        name="api_experience_detail",
    ),

    path(
        "api/v1/experience/<uuid:id>/star/",
        ExperienceStarAPIView.as_view(),
        name="api_experience_star",
    ),

    # =========================
    # EDUCATION
    # =========================

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

    path(
        "education/add-ajax/",
        create_education_ajax,
        name="create_education_ajax",
    ),

    path(
        "education/<int:education_id>/edit/",
        update_education,
        name="update_education"
    ),

    path(
        "education/<int:education_id>/delete/",
        delete_education,
        name="delete_education"
    ),

    path(
        "api/education/",
        get_education_json,
        name="get_education_json"
    ),

    # =========================
    # AUTH
    # =========================

    path(
        "login/",
        login_user,
        name="login"
    ),

    path(
        "logout/",
        logout_user,
        name="logout"
    ),
]
