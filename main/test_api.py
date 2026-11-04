from io import BytesIO
from pathlib import PurePosixPath
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient

from main.models import Experience


class ExperienceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse("main:api_experience_list_create")
        self.detail_url = reverse(
            "main:api_experience_detail",
            kwargs={"id": "00000000-0000-0000-0000-000000000001"},
        )
        self.user = User.objects.create_user("regular", password="password")
        self.editor = User.objects.create_user("editor", password="password")
        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)
        self.superuser = User.objects.create_superuser(
            "admin",
            password="password",
        )
        self.experience = Experience.objects.create(
            title="Existing experience",
            description="Existing description",
            category="research",
        )
        self.detail_url = reverse(
            "main:api_experience_detail",
            kwargs={"id": self.experience.id},
        )
        self.star_url = reverse(
            "main:api_experience_star",
            kwargs={"id": self.experience.id},
        )

    def valid_payload(self, **overrides):
        payload = {
            "title": "New experience",
            "description": "A useful project",
            "category": "internship",
        }
        payload.update(overrides)
        return payload

    def test_list_is_readable_by_every_role(self):
        for user in (None, self.user, self.editor, self.superuser):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]["id"], str(self.experience.id))
                self.assertTrue(response.data[0]["is_ongoing"])

    def test_create_is_superuser_only(self):
        for user in (None, self.user, self.editor):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(
                    self.list_url,
                    self.valid_payload(),
                    format="json",
                )
                self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            self.list_url,
            self.valid_payload(),
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Experience.objects.filter(title="New experience").exists()
        )

    def test_editor_and_superuser_can_update_but_regular_user_cannot(self):
        for user in (None, self.user):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.patch(
                    self.detail_url,
                    {"title": "Changed"},
                    format="json",
                )
                self.assertEqual(response.status_code, 403)

        for user in (self.editor, self.superuser):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.patch(
                    self.detail_url,
                    {"title": "Changed"},
                    format="json",
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["title"], "Changed")

    def test_put_and_read_only_fields(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(
            self.detail_url,
            self.valid_payload(
                started_at="2000-01-01T00:00:00Z",
                is_ongoing=False,
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            response.data["started_at"],
            "2000-01-01T00:00:00Z",
        )
        self.assertTrue(response.data["is_ongoing"])

    def test_editor_cannot_delete_and_superuser_can(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_unknown_uuid_returns_404(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse(
            "main:api_experience_detail",
            kwargs={"id": "00000000-0000-0000-0000-000000000099"},
        )
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_guest_cannot_put_or_delete_star(self):
        self.client.force_authenticate(user=None)

        put_response = self.client.put(self.star_url)
        delete_response = self.client.delete(self.star_url)

        self.assertEqual(put_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertFalse(self.experience.starred_by.exists())

    def test_authenticated_non_editor_can_put_and_delete_star(self):
        self.assertFalse(self.user.groups.filter(name="Editor").exists())
        self.client.force_authenticate(user=self.user)

        put_response = self.client.put(self.star_url)
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.data,
            {"star_count": 1, "is_starred": True},
        )

        delete_response = self.client.delete(self.star_url)
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            delete_response.data,
            {"star_count": 0, "is_starred": False},
        )

    def test_star_operations_are_idempotent_and_report_user_state(self):
        other_user = User.objects.create_user(
            "another-user",
            password="password",
        )
        self.experience.starred_by.add(other_user)
        self.client.force_authenticate(user=self.user)

        first_put = self.client.put(self.star_url)
        second_put = self.client.put(self.star_url)
        self.assertEqual(first_put.status_code, 200)
        self.assertEqual(second_put.status_code, 200)
        self.assertEqual(second_put.data["star_count"], 2)
        self.assertTrue(second_put.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 2)

        detail_after_put = self.client.get(self.detail_url)
        self.assertEqual(detail_after_put.data["star_count"], 2)
        self.assertTrue(detail_after_put.data["is_starred"])

        first_delete = self.client.delete(self.star_url)
        second_delete = self.client.delete(self.star_url)
        self.assertEqual(first_delete.status_code, 200)
        self.assertEqual(second_delete.status_code, 200)
        self.assertEqual(second_delete.data["star_count"], 1)
        self.assertFalse(second_delete.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 1)

        detail_after_delete = self.client.get(self.detail_url)
        self.assertEqual(detail_after_delete.data["star_count"], 1)
        self.assertFalse(detail_after_delete.data["is_starred"])
        self.assertTrue(
            self.experience.starred_by.filter(pk=other_user.pk).exists()
        )

    def test_star_api_unknown_experience_returns_404(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "main:api_experience_star",
            kwargs={"id": "00000000-0000-0000-0000-000000000099"},
        )

        self.assertEqual(self.client.put(url).status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)

    def test_star_api_rejects_other_methods(self):
        self.client.force_authenticate(user=self.user)

        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.post(self.star_url).status_code, 405)
        self.assertEqual(
            self.client.patch(self.star_url, {"is_starred": True}).status_code,
            405,
        )

    def test_star_session_authentication_requires_csrf(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        page_response = csrf_client.get(reverse("main:show_experience"))
        csrf_token = page_response.cookies["csrftoken"].value
        self.assertTrue(csrf_client.login(username="regular", password="password"))

        put_without_csrf = csrf_client.put(self.star_url)
        self.assertEqual(put_without_csrf.status_code, 403)

        put_with_csrf = csrf_client.put(
            self.star_url,
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(put_with_csrf.status_code, 200)

        delete_without_csrf = csrf_client.delete(self.star_url)
        self.assertEqual(delete_without_csrf.status_code, 403)

        delete_with_csrf = csrf_client.delete(
            self.star_url,
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(delete_with_csrf.status_code, 200)

    def test_non_uuid_path_does_not_match_detail_route(self):
        response = self.client.get("/api/experience/not-a-uuid/")
        self.assertEqual(response.status_code, 404)

    def test_session_authentication_requires_csrf_for_updates(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        page_response = csrf_client.get(reverse("main:show_experience"))
        csrf_token = page_response.cookies["csrftoken"].value
        self.assertTrue(csrf_client.login(username="editor", password="password"))

        response = csrf_client.patch(
            self.detail_url,
            {"title": "Changed without CSRF"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        response = csrf_client.patch(
            self.detail_url,
            {"title": "Changed with CSRF"},
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Changed with CSRF")

    def test_multipart_thumbnail_upload(self):
        image_buffer = BytesIO()
        Image.new("RGB", (2, 2), color="red").save(image_buffer, format="PNG")
        self.client.force_authenticate(user=self.superuser)

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    self.list_url,
                    self.valid_payload(
                        thumbnail=SimpleUploadedFile(
                            "thumbnail.png",
                            image_buffer.getvalue(),
                            content_type="image/png",
                        )
                    ),
                    format="multipart",
                )

        self.assertEqual(response.status_code, 201)
        thumbnail_url = response.data["thumbnail"]
        parsed_thumbnail_url = urlparse(thumbnail_url)
        thumbnail_path = parsed_thumbnail_url.path

        self.assertTrue(thumbnail_path)
        self.assertTrue(
            parsed_thumbnail_url.scheme in {"http", "https"}
            or thumbnail_path.startswith("/")
        )
        self.assertIn("/experience/", thumbnail_path)
        self.assertEqual(
            PurePosixPath(thumbnail_path).suffix.lower(),
            ".png",
        )

    def test_legacy_experience_json_route_remains_available(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["pk"], str(self.experience.id))

    def test_serializer_ignores_started_at_input(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            self.list_url,
            self.valid_payload(started_at="2000-01-01T00:00:00Z"),
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(
            response.data["started_at"],
            "2000-01-01T00:00:00Z",
        )
