from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout, login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime

from main.forms import EducationForm, ExperienceForm
from main.models import Experience, Education


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Akun berhasil dibuat. Silakan login."
        )

        return redirect("main:login")

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(
        request,
        "register.html",
        context
    )


def login_user(request):
    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        login(
            request,
            form.get_user()
        )

        response = redirect(
            "main:show_main"
        )

        response.set_cookie(
            "last_login",
            str(datetime.datetime.now())
        )

        return response

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(
        request,
        "login.html",
        context
    )


def logout_user(request):
    logout(request)

    response = redirect(
        "main:show_main"
    )

    response.delete_cookie(
        "last_login"
    )

    return response


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login"
    )

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "npm": "2506604794",
        "study_program": "S1 Sistem Informasi",
        "bio": "I'm interested in technology, business, and data. ",
        "last_login": last_login,
    }

    return render(
        request,
        "index.html",
        context
    )


def show_experience(request):
    is_editor = (
        request.user.is_authenticated
        and request.user.groups.filter(
            name="Editor"
        ).exists()
    )

    title_query = request.GET.get(
        "title",
        ""
    ).strip()

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "is_editor": is_editor,
        "title_query": title_query,
        "create_form": ExperienceForm(),
    }

    return render(
        request,
        "experience.html",
        context
    )


def get_experience_json(request):
    title_query = request.GET.get(
        "title",
        ""
    ).strip()

    experiences = (
        Experience.objects
        .prefetch_related("starred_by")
        .all()
    )

    if title_query:
        experiences = experiences.filter(
            title__icontains=title_query
        )

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.get_category_display(),
                "started_at": experience.started_at.strftime(
                    "%b %Y"
                ),
                "ended_at": (
                    experience.ended_at.strftime(
                        "%b %Y"
                    )
                    if experience.ended_at
                    else None
                ),
                "is_ongoing": experience.is_ongoing,
                "thumbnail_url": (
                    experience.thumbnail.url
                    if experience.thumbnail
                    else None
                ),
                "star_count": starred_users.count(),
                "is_starred": is_starred,
            },
        })

    return JsonResponse(
        data,
        safe=False
    )


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

        return redirect(
            "main:show_experience"
        )

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(
        request,
        "experience_form.html",
        context
    )


@require_POST
def create_experience_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang "
                    "dapat menambahkan experience."
                )
            },
            status=403
        )

    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang "
                    "dapat menambahkan experience."
                )
            },
            status=403
        )

    form = ExperienceForm(
        request.POST,
        request.FILES
    )

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                "message": (
                    "Experience berhasil ditambahkan."
                ),
                "pk": str(experience.id),
            },
            status=201
        )

    return JsonResponse(
        {
            "errors": form.errors.get_json_data()
        },
        status=400
    )


@login_required
def update_experience(
    request,
    experience_id
):
    is_editor = request.user.groups.filter(
        name="Editor"
    ).exists()

    if (
        not request.user.is_superuser
        and not is_editor
    ):
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

        return redirect(
            "main:show_experience"
        )

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
def delete_experience(
    request,
    experience_id
):
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

        return redirect(
            "main:show_experience"
        )

    return redirect(
        "main:show_experience"
    )


def show_education(request):
    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "institution_query": institution_query,
        "create_form": EducationForm(),
    }

    return render(request,
        "education.html", context)


def get_education_json(request):

    # Data pendidikan dikirim sebagai JSON agar frontend dapat
    # mengambil dan merender daftar pendidikan menggunakan AJAX
    # tanpa melakukan reload halaman.
    institution_query = request.GET.get(
        "institution",
        ""
    ).strip()

    educations = (
        Education.objects
        .all()
        .order_by("-id")
    )

    # Filter hanya diterapkan ketika pengguna memasukkan kata pencarian,
    # sehingga tanpa query seluruh data pendidikan tetap ditampilkan.
    if institution_query:
        educations = educations.filter(
            institution__icontains=institution_query
        )

    data = []

    # Hanya field yang dibutuhkan frontend yang dikirim melalui response
    # untuk menjaga struktur data tetap sederhana dan mudah dirender.
    for education in educations:
        data.append({
            "pk": education.pk,
            "fields": {
                "institution": education.institution,
                "degree": education.degree,
                "year": education.year,
                "graduation_year": education.graduation_year,
            },
        })

    return JsonResponse(
        data,
        safe=False
    )


@login_required
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Data pendidikan berhasil ditambahkan!"
        )

        return redirect(
            "main:show_education"
        )

    context = {
        "name": "Banin Shula Afiqah Aradena",
        "form": form,
    }

    return render(
        request,
        "education_form.html",
        context
    )

@require_POST
def create_education_ajax(request):
    # Endpoint tetap melakukan pemeriksaan akses di server.
    # Menyembunyikan tombol pada template saja tidak cukup untuk
    # mencegah pengguna lain mengirim request secara langsung.
    # Hanya pemilik portfolio yang boleh menambahkan data Education.
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang "
                    "dapat menambahkan pendidikan."
                )
            },
            status=403,
        )

    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang "
                    "dapat menambahkan pendidikan."
                )
            },
            status=403,
        )

    # ModelForm yang sama digunakan kembali agar validasi AJAX
    # konsisten dengan validasi data pendidikan lainnya.
    form = EducationForm(request.POST)

    # Data hanya disimpan jika seluruh validasi server-side berhasil.
    if form.is_valid():
        education = form.save()

        # Status 201 menunjukkan bahwa data baru berhasil dibuat,
        # sehingga frontend dapat membedakannya dari response error.
        return JsonResponse(
            {
                "message": "Pendidikan berhasil ditambahkan.",
                "pk": education.pk,
            },
            status=201,
        )

    # Error validasi dikirim kembali dalam format JSON agar frontend
    # dapat menampilkan kegagalan tanpa melakukan reload halaman.
    return JsonResponse(
        {
            "errors": form.errors.get_json_data()
        },
        status=400,
    )


@login_required
def update_education(
    request,
    education_id
):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(
        Education,
        pk=education_id
    )

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

        return redirect(
            "main:show_education"
        )

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


@login_required
def delete_education(
    request,
    education_id
):
    if not request.user.is_superuser:
        raise PermissionDenied

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

        return redirect(
            "main:show_education"
        )

    return redirect(
        "main:show_education"
    )


@login_required(login_url="/login/")
def toggle_star(
    request,
    experience_id
):
    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(
                request.user
            )
        else:
            experience.starred_by.add(
                request.user
            )

    return redirect(
        "main:show_experience"
    )
