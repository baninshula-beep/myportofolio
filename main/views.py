from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import EducationForm
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
    institution_query = request.GET.get("institution", "").strip()

    education_list = Education.objects.all()

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "education_list": education_list,
        "institution_query": institution_query,
    }

    return render(request, "education.html", context)


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Data pendidikan berhasil ditambahkan!"
        )
        return redirect("main:show_education")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(request, "education_form.html", context)


def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()

    education_list = Education.objects.all()

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    education_json = serializers.serialize(
        "json",
        education_list
    )

    return HttpResponse(
        education_json,
        content_type="application/json"
    )


def delete_education(request, education_id):
    education = get_object_or_404(
        Education,
        pk=education_id
    )

    if request.method == "POST":
        education.delete()

        messages.success(
            request,
            "Data pendidikan berhasil dihapus!"
        )

        return redirect("main:show_education")

    return redirect("main:show_education")