from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience


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
