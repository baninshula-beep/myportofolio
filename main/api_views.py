from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Experience
from main.permissions import ExperiencePermission
from main.serializers import ExperienceSerializer


class ExperienceListCreateAPIView(ListCreateAPIView):
    queryset = Experience.objects.prefetch_related("starred_by").all()
    serializer_class = ExperienceSerializer
    permission_classes = [ExperiencePermission]
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class ExperienceDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.prefetch_related("starred_by").all()
    serializer_class = ExperienceSerializer
    permission_classes = [ExperiencePermission]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = "id"
    lookup_url_kwarg = "id"


class ExperienceStarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        with transaction.atomic():
            experience = get_object_or_404(
                Experience.objects.select_for_update(),
                pk=id,
            )
            is_starred = experience.starred_by.filter(
                pk=request.user.pk
            ).exists()

            if is_starred:
                experience.starred_by.remove(request.user)
            else:
                experience.starred_by.add(request.user)

            is_starred = experience.starred_by.filter(
                pk=request.user.pk
            ).exists()
            star_count = experience.starred_by.count()

        return Response({
            "star_count": star_count,
            "is_starred": is_starred,
        })
