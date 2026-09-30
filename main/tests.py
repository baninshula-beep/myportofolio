from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.superuser = User.objects.create_superuser(
            username="superuser",
            password="superpassword123",
        )

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"',
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

        # Experience data is now loaded through the AJAX endpoint.
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="grid"')

        # The page should no longer render experience data directly.
        self.assertNotContains(response, self.experience.title)

    def test_experience_json(self):
        response = self.client.get(
            reverse("main:get_experience_json")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/json",
        )

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["pk"],
            str(self.experience.id),
        )
        self.assertEqual(
            data[0]["fields"]["title"],
            self.experience.title,
        )
        self.assertEqual(
            data[0]["fields"]["description"],
            self.experience.description,
        )
        self.assertEqual(
            data[0]["fields"]["category"],
            "Part-Time",
        )
        self.assertTrue(
            data[0]["fields"]["is_ongoing"]
        )
        self.assertIsNone(
            data[0]["fields"]["ended_at"]
        )
        self.assertEqual(
            data[0]["fields"]["star_count"],
            0,
        )
        self.assertFalse(
            data[0]["fields"]["is_starred"]
        )

    def test_experience_json_with_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        response = self.client.get(
            reverse("main:get_experience_json")
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertFalse(
            data[0]["fields"]["is_ongoing"]
        )
        self.assertIsNotNone(
            data[0]["fields"]["ended_at"]
        )

    def test_experience_json_search(self):
        Experience.objects.create(
            title="COMPFEST 18",
            description="Marketing and Business Development.",
            category="part-time",
        )

        response = self.client.get(
            reverse("main:get_experience_json"),
            {"title": "COMPFEST"},
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["fields"]["title"],
            "COMPFEST 18",
        )

    def test_create_experience_ajax_success(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "COMPFEST 18",
                "description": "Marketing and Business Development",
                "category": "part-time",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.json()

        self.assertIn("pk", data)
        self.assertEqual(
            data["message"],
            "Experience berhasil ditambahkan.",
        )

        self.assertTrue(
            Experience.objects.filter(
                title="COMPFEST 18"
            ).exists()
        )


    def test_create_experience_ajax_forbidden(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "Unauthorized Experience",
                "description": "Should not be created",
                "category": "part-time",
            },
        )

        self.assertEqual(response.status_code, 403)

        data = response.json()

        self.assertEqual(
            data["message"],
            "Hanya pemilik portofolio yang dapat menambahkan experience.",
        )

        self.assertFalse(
            Experience.objects.filter(
                title="Unauthorized Experience"
            ).exists()
        )


    def test_create_experience_ajax_invalid(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {
                "title": "",
                "description": "Invalid experience",
                "category": "part-time",
            },
        )

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertIn(
            "errors",
            data,
        )

        self.assertIn(
            "title",
            data["errors"],
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertEqual(response.status_code, 200)

        # Empty state is now handled by JavaScript
        # after receiving an empty AJAX response.
        self.assertContains(response, 'id="empty"')

    def test_empty_experience_json(self):
        Experience.objects.all().delete()

        response = self.client.get(
            reverse("main:get_experience_json")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        response = self.client.get(
            reverse("main:get_experience_json")
        )

        data = response.json()

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(
            data[0]["fields"]["is_ongoing"]
        )

    def test_education_url_and_template(self):
        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
        )

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertContains(response, education.institution)
        self.assertContains(response, education.degree)
        self.assertContains(response, education.year)

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertContains(
            response,
            "Belum ada data pendidikan yang ditambahkan.",
        )

    def test_education_with_graduation_year(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
            graduation_year=2028,
        )

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertContains(
            response,
            str(education.graduation_year),
        )

    def test_create_education(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("main:create_education"),
            {
                "institution": "Universitas Indonesia",
                "degree": "S1 Sistem Informasi",
                "year": "2024 - Present",
                "graduation_year": 2028,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Education.objects.filter(
                institution="Universitas Indonesia"
            ).exists()
        )

    def test_update_education(self):
        self.client.force_login(self.user)

        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
            graduation_year=2028,
        )

        response = self.client.post(
            reverse(
                "main:update_education",
                args=[education.id],
            ),
            {
                "institution": "Universitas Indonesia",
                "degree": "S1 Ilmu Komputer",
                "year": "2024 - Present",
                "graduation_year": 2028,
            },
        )

        self.assertEqual(response.status_code, 302)

        education.refresh_from_db()

        self.assertEqual(
            education.degree,
            "S1 Ilmu Komputer",
        )

    def test_delete_education(self):
        self.client.force_login(self.user)

        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
            graduation_year=2028,
        )

        response = self.client.post(
            reverse(
                "main:delete_education",
                args=[education.id],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Education.objects.filter(
                id=education.id
            ).exists()
        )

    def test_education_json(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
        )

        response = self.client.get(
            reverse("main:get_education_json")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/json",
        )

        data = response.json()

        self.assertEqual(
            data[0]["fields"]["institution"],
            education.institution,
        )
        self.assertEqual(
            data[0]["fields"]["graduation_year"],
            education.graduation_year,
        )