from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
import datetime
from django.contrib.auth.decorators import login_required

from main.forms import EducationForm, ExperienceForm
from main.models import Experience, Education
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())

        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            str(datetime.datetime.now())
        )

        return response

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(request, "login.html", context)

def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")

    return response

def show_main(request):
    last_login = request.COOKIES.get("last_login")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "npm": "2506604794",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I'm interested in technology, business, and data. "
        ),
        "last_login": last_login,
    }

    return render(request, "index.html", context)


def show_experience(request):
    is_editor = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Editor").exists()
    )

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "experience_list": Experience.objects.all(),
        "is_editor": is_editor,
    }

    return render(request, "experience.html", context)

@login_required
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Pengalaman berhasil ditambahkan!"
        )

        return redirect("main:show_experience")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(
        request,
        "experience_form.html",
        context
    )


@login_required
def update_experience(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not request.user.is_superuser and not is_editor:
        raise PermissionDenied

    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    form = ExperienceForm(
        request.POST or None,
        request.FILES or None,
        instance=experience
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Pengalaman berhasil diperbarui!"
        )

        return redirect("main:show_experience")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
        "experience": experience,
    }

    return render(
        request,
        "experience_form.html",
        context
    )


@login_required
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.method == "POST":
        experience.delete()

        messages.success(
            request,
            "Pengalaman berhasil dihapus!"
        )

        return redirect("main:show_experience")

    return redirect("main:show_experience")

def show_education(request):
    institution_query = request.GET.get("institution", "").strip()

    education_list = Education.objects.all()

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    # Serialisasi data Education menjadi JSON sebelum ditampilkan.
    education_json = serializers.serialize(
        "json",
        education_list
    )

    # Data JSON dideserialisasi kembali menjadi object Education
    # agar dapat digunakan oleh template untuk menampilkan data.
    education_list = list(
        serializers.deserialize(
            "json",
            education_json
        )
    )

    education_list = [
        item.object
        for item in education_list
    ]

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "education_list": education_list,
        "institution_query": institution_query,
    }

    return render(request, "education.html", context)

@login_required
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

@login_required
def update_education(request, education_id):

    # Mengambil data Education berdasarkan ID dan mengembalikan 404
    # jika data yang diminta tidak ditemukan.
    education = get_object_or_404(
        Education,
        pk=education_id
    )

    # Instance yang ditemukan digunakan agar form mengedit data lama,
    # bukan membuat data Education baru.
    form = EducationForm(
        request.POST or None,
        instance=education
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Data pendidikan berhasil diperbarui!"
        )

        return redirect("main:show_education")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
        "education": education,
    }

    return render(
        request,
        "education_form.html",
        context
    )

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()

    education_list = Education.objects.all()

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    # Mengubah queryset Education menjadi JSON agar data dapat
    # diakses melalui endpoint API.
    education_json = serializers.serialize(
        "json",
        education_list
    )

    return HttpResponse(
        education_json,
        content_type="application/json"
    )

@login_required
def delete_education(request, education_id):

    # Mengambil data yang akan dihapus berdasarkan ID.
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

@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")
