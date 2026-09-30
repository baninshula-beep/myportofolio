from django.urls import path

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
)


app_name = "main"


urlpatterns = [
    path("", show_main, name="show_main"),

    path(
        "register/",
        register,
        name="register"
    ),

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
        "experience/",
        show_experience,
        name="show_experience"
    ),

    path(
        "api/experience/",
        get_experience_json,
        name="get_experience_json"
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