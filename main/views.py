from django.shortcuts import render
from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Banin Shula Afiqah Aradena",
        "npm": "2506604794",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada teknologi, data, dan pengembangan produk."
        ),
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Banin Shula Afiqah Aradena",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Banin Shula Afiqah Aradena",
        "education_list": Education.objects.all(),
    }

    return render(request, "education.html", context)