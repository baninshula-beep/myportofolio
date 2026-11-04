from django.contrib.auth.models import AnonymousUser, Group, User
from django.test import TestCase
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIRequestFactory

from main.permissions import ExperiencePermission


class ExperiencePermissionTests(TestCase):
    methods = ("GET", "POST", "PUT", "PATCH", "DELETE")

    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = ExperiencePermission()
        self.guest = AnonymousUser()
        self.user = User.objects.create_user(
            username="regular",
            password="password",
        )
        self.editor = User.objects.create_user(
            username="editor",
            password="password",
        )
        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)
        self.superuser = User.objects.create_superuser(
            username="admin",
            password="password",
        )

    def permission_result(self, role, method):
        request = getattr(self.factory, method.lower())("/api/experience/")
        request.user = role
        return self.permission.has_permission(request, view=None)

    def test_guest_access_matrix(self):
        allowed = {"GET"}
        for method in self.methods:
            with self.subTest(method=method):
                self.assertEqual(
                    self.permission_result(self.guest, method),
                    method in allowed,
                )

    def test_authenticated_user_access_matrix(self):
        allowed = {"GET"}
        for method in self.methods:
            with self.subTest(method=method):
                self.assertEqual(
                    self.permission_result(self.user, method),
                    method in allowed,
                )

    def test_editor_access_matrix(self):
        allowed = {"GET", "PUT", "PATCH"}
        for method in self.methods:
            with self.subTest(method=method):
                self.assertEqual(
                    self.permission_result(self.editor, method),
                    method in allowed,
                )

    def test_superuser_access_matrix(self):
        for method in self.methods:
            with self.subTest(method=method):
                self.assertTrue(
                    self.permission_result(self.superuser, method)
                )

    def test_star_permission_is_authenticated_only(self):
        star_permission = IsAuthenticated()
        guest_request = self.factory.post("/api/experience/star/")
        guest_request.user = self.guest
        user_request = self.factory.post("/api/experience/star/")
        user_request.user = self.user

        self.assertFalse(star_permission.has_permission(guest_request, None))
        self.assertTrue(star_permission.has_permission(user_request, None))
