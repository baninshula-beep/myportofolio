from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
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
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan."
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_education_url_and_template(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, education.institution)
        self.assertContains(response, education.degree)
        self.assertContains(response, education.year)

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "Belum ada data pendidikan yang ditambahkan."
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
            str(education.graduation_year)
        )

    def test_create_education(self):
        response = self.client.post(
            reverse("main:create_education"),
            {
                "institution": "Universitas Indonesia",
                "degree": "S1 Sistem Informasi",
                "year": "2024 - Present",
                "graduation_year": 2028,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Education.objects.filter(
                institution="Universitas Indonesia"
            ).exists()
        )

    def test_update_education(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
            graduation_year=2028,
        )

        response = self.client.post(
            reverse(
                "main:update_education",
                args=[education.id]
            ),
            {
                "institution": "Universitas Indonesia",
                "degree": "S1 Ilmu Komputer",
                "year": "2024 - Present",
                "graduation_year": 2028,
            }
        )

        self.assertEqual(response.status_code, 302)

        education.refresh_from_db()

        self.assertEqual(
            education.degree,
            "S1 Ilmu Komputer"
        )

    def test_delete_education(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
            graduation_year=2028,
        )

        response = self.client.post(
            reverse(
                "main:delete_education",
                args=[education.id]
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
            graduation_year=2028,
        )

        response = self.client.get(
            reverse("main:get_education_json")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/json"
        )
        self.assertContains(
            response,
            education.institution
        )
        self.assertContains(
            response,
            str(education.graduation_year)
        )