from django.shortcuts import get_object_or_404
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

    def put(self, request, id):
        experience = get_object_or_404(Experience, pk=id)
        experience.starred_by.add(request.user)

        return Response({
            "star_count": experience.starred_by.count(),
            "is_starred": True,
        })

    def delete(self, request, id):
        experience = get_object_or_404(Experience, pk=id)
        experience.starred_by.remove(request.user)

        return Response({
            "star_count": experience.starred_by.count(),
            "is_starred": False,
        })
