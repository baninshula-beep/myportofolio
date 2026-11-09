from io import BytesIO
from pathlib import PurePosixPath
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

from django.contrib.auth.models import AnonymousUser, Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience


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

    def test_guest_cannot_toggle_star(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.experience.starred_by.exists())

    def test_authenticated_non_editor_can_toggle_star(self):
        self.assertFalse(self.user.groups.filter(name="Editor").exists())
        self.client.force_authenticate(user=self.user)

        star_response = self.client.post(self.star_url)
        self.assertEqual(star_response.status_code, 200)
        self.assertEqual(
            star_response.data,
            {"star_count": 1, "is_starred": True},
        )

        unstar_response = self.client.post(self.star_url)
        self.assertEqual(unstar_response.status_code, 200)
        self.assertEqual(
            unstar_response.data,
            {"star_count": 0, "is_starred": False},
        )

    def test_star_post_toggles_state_and_reports_user_state(self):
        other_user = User.objects.create_user(
            "another-user",
            password="password",
        )
        self.experience.starred_by.add(other_user)
        self.client.force_authenticate(user=self.user)

        star_response = self.client.post(self.star_url)
        self.assertEqual(star_response.status_code, 200)
        self.assertEqual(star_response.data["star_count"], 2)
        self.assertTrue(star_response.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 2)

        detail_after_star = self.client.get(self.detail_url)
        self.assertEqual(detail_after_star.data["star_count"], 2)
        self.assertTrue(detail_after_star.data["is_starred"])

        unstar_response = self.client.post(self.star_url)
        self.assertEqual(unstar_response.status_code, 200)
        self.assertEqual(unstar_response.data["star_count"], 1)
        self.assertFalse(unstar_response.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 1)

        detail_after_unstar = self.client.get(self.detail_url)
        self.assertEqual(detail_after_unstar.data["star_count"], 1)
        self.assertFalse(detail_after_unstar.data["is_starred"])
        self.assertTrue(
            self.experience.starred_by.filter(pk=other_user.pk).exists()
        )

    def test_starred_usernames_are_not_exposed_in_any_experience_response(self):
        self.experience.starred_by.add(self.user)
        legacy_url = reverse("main:get_experience_json")

        for user in (None, self.user):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)

                list_response = self.client.get(self.list_url)
                self.assertEqual(list_response.status_code, 200)
                self.assertNotIn(
                    "starred_by_names",
                    list_response.data[0],
                )
                self.assertNotIn(self.user.username, str(list_response.data))

                detail_response = self.client.get(self.detail_url)
                self.assertEqual(detail_response.status_code, 200)
                self.assertNotIn(
                    "starred_by_names",
                    detail_response.data,
                )
                self.assertNotIn(self.user.username, str(detail_response.data))

                legacy_response = self.client.get(legacy_url)
                self.assertEqual(legacy_response.status_code, 200)
                self.assertNotIn(
                    "starred_by_names",
                    legacy_response.json()[0]["fields"],
                )
                self.assertNotIn(self.user.username, legacy_response.content.decode())

    def test_star_api_unknown_experience_returns_404(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "main:api_experience_star",
            kwargs={"id": "00000000-0000-0000-0000-000000000099"},
        )

        self.assertEqual(self.client.post(url).status_code, 404)

    def test_star_api_rejects_other_methods(self):
        self.client.force_authenticate(user=self.user)

        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.put(self.star_url).status_code, 405)
        self.assertEqual(self.client.delete(self.star_url).status_code, 405)
        self.assertEqual(
            self.client.patch(self.star_url, {"is_starred": True}).status_code,
            405,
        )

    def test_star_session_authentication_requires_csrf(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        page_response = csrf_client.get(reverse("main:show_experience"))
        csrf_token = page_response.cookies["csrftoken"].value
        self.assertTrue(csrf_client.login(username="regular", password="password"))

        post_without_csrf = csrf_client.post(self.star_url)
        self.assertEqual(post_without_csrf.status_code, 403)
        self.assertFalse(self.experience.starred_by.filter(pk=self.user.pk).exists())

        post_with_csrf = csrf_client.post(
            self.star_url,
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(post_with_csrf.status_code, 200)
        self.assertTrue(self.experience.starred_by.filter(pk=self.user.pk).exists())

        post_without_csrf = csrf_client.post(self.star_url)
        self.assertEqual(post_without_csrf.status_code, 403)

        post_with_csrf = csrf_client.post(
            self.star_url,
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(post_with_csrf.status_code, 200)
        self.assertFalse(self.experience.starred_by.filter(pk=self.user.pk).exists())

    def test_non_uuid_path_does_not_match_detail_route(self):
        response = self.client.get("/api/v1/experience/not-a-uuid/")
        self.assertEqual(response.status_code, 404)

    def test_api_uses_v1_prefix_without_old_routes(self):
        self.assertEqual(self.list_url, "/api/v1/experience/")
        self.assertEqual(
            self.detail_url,
            f"/api/v1/experience/{self.experience.id}/",
        )
        self.assertEqual(
            self.star_url,
            f"/api/v1/experience/{self.experience.id}/star/",
        )
        for old_url in (
            "/api/experience/",
            f"/api/experience/{self.experience.id}/",
            f"/api/experience/{self.experience.id}/star/",
        ):
            with self.subTest(url=old_url):
                self.assertEqual(self.client.get(old_url).status_code, 404)

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


class EducationAPITests(APITestCase):
    """Exercise Education API behavior across roles and authentication paths."""

    def setUp(self):
        self.client = APIClient()
        self.visitor = AnonymousUser()
        self.user = User.objects.create_user(
            username="education-user",
            email="education-user@example.com",
            password="password",
        )
        self.editor = User.objects.create_user(
            username="education-editor",
            password="password",
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)
        self.superuser = User.objects.create_superuser(
            username="education-owner",
            email="education-owner@example.com",
            password="password",
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            year="2024 - Present",
            graduation_year=2028,
        )
        self.list_url = reverse("main:api_education_list_create")
        self.detail_url = reverse(
            "main:api_education_detail",
            kwargs={"education_id": self.education.pk},
        )
        self.star_url = reverse(
            "main:api_education_star",
            kwargs={"education_id": self.education.pk},
        )

    def valid_payload(self, **overrides):
        payload = {
            "institution": "Universitas Gadjah Mada",
            "degree": "S1 Informatika",
            "year": "2025 - Present",
            "graduation_year": 2029,
        }
        payload.update(overrides)
        return payload

    def assert_write_denied_without_changes(self, user, operations):
        """Check authorization and persisted state after every rejected write."""
        self.client.force_authenticate(user=user)
        self.education.refresh_from_db()
        initial_count = Education.objects.count()
        initial_values = (
            self.education.institution,
            self.education.degree,
            self.education.year,
            self.education.graduation_year,
        )
        initial_starred_ids = set(
            self.education.starred_by.values_list("pk", flat=True)
        )

        for method, url, payload in operations:
            with self.subTest(user=user, method=method, url=url):
                request = getattr(self.client, method.lower())
                kwargs = {}
                if payload is not None:
                    kwargs.update(data=payload, format="json")
                response = request(url, **kwargs)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(Education.objects.count(), initial_count)

                self.education.refresh_from_db()
                self.assertEqual(
                    (
                        self.education.institution,
                        self.education.degree,
                        self.education.year,
                        self.education.graduation_year,
                    ),
                    initial_values,
                )
                self.assertEqual(
                    set(
                        self.education.starred_by.values_list("pk", flat=True)
                    ),
                    initial_starred_ids,
                )

    def crud_write_operations(self):
        return [
            ("POST", self.list_url, self.valid_payload()),
            ("PUT", self.detail_url, self.valid_payload()),
            ("PATCH", self.detail_url, {"degree": "Updated degree"}),
            ("DELETE", self.detail_url, None),
        ]

    def test_visitor_can_read_list_and_detail(self):
        self.education.starred_by.add(self.user)

        list_response = self.client.get(self.list_url)
        detail_response = self.client.get(self.detail_url)

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)
        self.assertFalse(list_response.data[0]["is_starred"])
        self.assertFalse(detail_response.data["is_starred"])
        self.assertEqual(detail_response.data["star_count"], 1)

    def test_visitor_cannot_mutate_education(self):
        self.assert_write_denied_without_changes(
            self.visitor,
            self.crud_write_operations(),
        )

    def test_normal_user_cannot_use_education_crud(self):
        self.assert_write_denied_without_changes(
            self.user,
            self.crud_write_operations(),
        )

    def test_normal_user_can_star_and_unstar_education(self):
        self.client.force_authenticate(user=self.user)

        star_response = self.client.post(self.star_url)
        self.assertEqual(star_response.status_code, 200)
        self.assertEqual(
            star_response.data,
            {"star_count": 1, "is_starred": True},
        )
        self.assertTrue(
            self.education.starred_by.filter(pk=self.user.pk).exists()
        )

        unstar_response = self.client.post(self.star_url)
        self.assertEqual(unstar_response.status_code, 200)
        self.assertEqual(
            unstar_response.data,
            {"star_count": 0, "is_starred": False},
        )
        self.assertFalse(self.education.starred_by.exists())

    def test_editor_can_put_and_patch_but_cannot_post_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        put_response = self.client.put(
            self.detail_url,
            self.valid_payload(institution="Updated Institution"),
            format="json",
        )
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.data["institution"], "Updated Institution")

        patch_response = self.client.patch(
            self.detail_url,
            {"degree": "Updated degree"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data["degree"], "Updated degree")

        self.assert_write_denied_without_changes(
            self.editor,
            [
                ("POST", self.list_url, self.valid_payload()),
                ("DELETE", self.detail_url, None),
            ],
        )

    def test_superuser_can_create_and_delete_education(self):
        self.client.force_authenticate(user=self.superuser)

        create_response = self.client.post(
            self.list_url,
            self.valid_payload(),
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        created_id = create_response.data["id"]
        self.assertTrue(Education.objects.filter(pk=created_id).exists())

        delete_response = self.client.delete(
            reverse(
                "main:api_education_detail",
                kwargs={"education_id": created_id},
            )
        )
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Education.objects.filter(pk=created_id).exists())

    def test_invalid_input_and_html_only_text_are_rejected(self):
        self.client.force_authenticate(user=self.superuser)
        initial_count = Education.objects.count()

        invalid_payloads = [
            {"institution": "", "degree": "Valid degree", "year": "2025"},
            {
                "institution": "Valid institution",
                "degree": "Valid degree",
                "year": "<b></b>",
            },
            {
                "institution": "Valid institution",
                "degree": "<i> </i>",
                "year": "2025",
            },
            {
                "institution": "<p><br></p>",
                "degree": "Valid degree",
                "year": "2025",
            },
            self.valid_payload(graduation_year="not-a-year"),
        ]

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(
                    self.list_url,
                    payload,
                    format="json",
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(Education.objects.count(), initial_count)

    def test_valid_html_tags_are_stripped_from_text(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            self.list_url,
            self.valid_payload(
                institution="<b>Universitas Gadjah Mada</b>",
                degree="<i>S1 Informatika</i>",
                year="<span>2025</span>",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["institution"],
            "Universitas Gadjah Mada",
        )
        self.assertEqual(response.data["degree"], "S1 Informatika")
        self.assertEqual(response.data["year"], "2025")

    def test_star_fields_are_read_only_and_visitor_state_is_false(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            self.list_url,
            self.valid_payload(star_count=999, is_starred=True),
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

        created = Education.objects.get(pk=response.data["id"])
        self.client.force_authenticate(user=self.superuser)
        update_response = self.client.patch(
            reverse(
                "main:api_education_detail",
                kwargs={"education_id": created.pk},
            ),
            {"star_count": 45, "is_starred": True},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.client.force_authenticate(user=None)
        detail_response = self.client.get(
            reverse(
                "main:api_education_detail",
                kwargs={"education_id": created.pk},
            )
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data["star_count"], 0)
        self.assertFalse(detail_response.data["is_starred"])

    def test_institution_search_filters_results(self):
        Education.objects.create(
            institution="Stanford University",
            degree="MSc Computer Science",
            year="2025 - 2027",
        )

        response = self.client.get(
            self.list_url,
            {"institution": "stanford"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["institution"],
            "Stanford University",
        )

    def test_missing_detail_and_star_targets_return_404(self):
        self.client.force_authenticate(user=self.user)
        missing_detail_url = reverse(
            "main:api_education_detail",
            kwargs={"education_id": self.education.pk + 1000},
        )
        missing_star_url = reverse(
            "main:api_education_star",
            kwargs={"education_id": self.education.pk + 1000},
        )

        self.assertEqual(self.client.get(missing_detail_url).status_code, 404)
        self.assertEqual(self.client.post(missing_star_url).status_code, 404)

    def test_visitor_cannot_use_star_endpoint(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.education.starred_by.exists())

    def test_star_only_changes_requesting_user_and_exposes_no_user_data(self):
        other_user = User.objects.create_user(
            username="education-other-starred-user",
            email="private@example.com",
            password="private-password",
        )
        self.education.starred_by.add(other_user)
        self.client.force_authenticate(user=self.user)

        star_response = self.client.post(self.star_url)
        self.assertEqual(star_response.status_code, 200)
        self.assertEqual(star_response.data["star_count"], 2)
        self.assertTrue(star_response.data["is_starred"])
        self.assertEqual(
            set(self.education.starred_by.values_list("pk", flat=True)),
            {self.user.pk, other_user.pk},
        )

        response_text = str(star_response.data)
        for private_value in (
            self.user.username,
            self.user.email,
            self.user.password,
            other_user.username,
            other_user.email,
            other_user.password,
        ):
            self.assertNotIn(private_value, response_text)

        unstar_response = self.client.post(self.star_url)
        self.assertEqual(unstar_response.status_code, 200)
        self.assertEqual(unstar_response.data["star_count"], 1)
        self.assertFalse(unstar_response.data["is_starred"])
        self.assertEqual(
            list(self.education.starred_by.values_list("pk", flat=True)),
            [other_user.pk],
        )

    def test_star_endpoint_rejects_unsupported_methods_without_changes(self):
        self.client.force_authenticate(user=self.user)
        initial_starred_ids = set(
            self.education.starred_by.values_list("pk", flat=True)
        )

        responses = [
            self.client.get(self.star_url),
            self.client.put(self.star_url, {}, format="json"),
            self.client.patch(self.star_url, {}, format="json"),
            self.client.delete(self.star_url),
        ]

        for response in responses:
            self.assertEqual(response.status_code, 405)
        self.assertEqual(
            set(self.education.starred_by.values_list("pk", flat=True)),
            initial_starred_ids,
        )

    def test_session_mutations_require_csrf_token(self):
        # Use a real session login with CSRF enforcement: force_authenticate
        # bypasses middleware/authentication checks and cannot prove CSRF works.
        csrf_client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            csrf_client.login(
                username="education-owner",
                password="password",
            )
        )
        # Fetch the token after login because Django rotates it on login.
        page_response = csrf_client.get(reverse("main:show_education"))
        csrf_token = page_response.cookies["csrftoken"].value
        initial_count = Education.objects.count()

        rejected_create = csrf_client.post(
            self.list_url,
            self.valid_payload(),
            format="json",
        )
        self.assertEqual(rejected_create.status_code, 403)
        self.assertEqual(Education.objects.count(), initial_count)

        rejected_update = csrf_client.patch(
            self.detail_url,
            {"degree": "Should not persist"},
            format="json",
        )
        self.assertEqual(rejected_update.status_code, 403)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Sistem Informasi")

        accepted_create = csrf_client.post(
            self.list_url,
            self.valid_payload(),
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(accepted_create.status_code, 201)
