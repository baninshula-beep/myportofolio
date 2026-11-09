from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Experience


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer for public Experience data and validated Experience input.
    """

    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(
        max_length=255,
        allow_blank=True,
    )
    started_at = serializers.DateTimeField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "is_ongoing",
            "star_count",
            "is_starred",
        ]
        read_only_fields = [
            "id",
            "started_at",
            "is_ongoing",
            "star_count",
            "is_starred",
        ]

    def validate_title(self, value):
        title = strip_tags(value).strip()

        if not title:
            raise serializers.ValidationError(
                "Judul experience tidak boleh hanya berisi tag HTML."
            )

        return title

    def validate_description(self, value):
        description = strip_tags(value).strip()

        if not description:
            raise serializers.ValidationError(
                "Deskripsi experience tidak boleh kosong atau hanya berisi tag HTML."
            )

        return description

    def get_star_count(self, obj):
        if obj.pk is None:
            return 0

        return obj.starred_by.count()

    def get_is_starred(self, obj):
        if obj.pk is None:
            return False

        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not getattr(user, "is_authenticated", False):
            return False

        return obj.starred_by.filter(pk=user.pk).exists()


class EducationSerializer(serializers.ModelSerializer):
    """Serialize Education fields and the requesting user's star state."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "year",
            "graduation_year",
            "star_count",
            "is_starred",
        ]
        read_only_fields = ["id", "star_count", "is_starred"]

    def validate_institution(self, value):
        institution = strip_tags(value).strip()
        if not institution:
            raise serializers.ValidationError(
                "Nama institusi tidak boleh kosong atau hanya berisi tag HTML."
            )
        return institution

    def validate_degree(self, value):
        degree = strip_tags(value).strip()
        if not degree:
            raise serializers.ValidationError(
                "Gelar tidak boleh kosong atau hanya berisi tag HTML."
            )
        return degree

    def validate_year(self, value):
        year = strip_tags(value).strip()
        if not year:
            raise serializers.ValidationError(
                "Tahun tidak boleh kosong atau hanya berisi tag HTML."
            )
        return year

    def get_star_count(self, obj):
        return obj.starred_by.all().count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return False

        return any(
            starred_user.pk == user.pk
            for starred_user in obj.starred_by.all()
        )
