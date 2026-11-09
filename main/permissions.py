from rest_framework.permissions import BasePermission, SAFE_METHODS


class ExperiencePermission(BasePermission):
    """Allow public reads, Editor updates, and full superuser access."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return (
            request.method in ("PUT", "PATCH")
            and user.groups.filter(name="Editor").exists()
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Allow public reads, Editor updates, and full superuser CRUD access.

    Star access is checked separately by the dedicated authenticated endpoint,
    so it does not grant users permission to modify Education fields.
    """

    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return (
            request.method in ("PUT", "PATCH")
            and user.groups.filter(name="Editor").exists()
        )
