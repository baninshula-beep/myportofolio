from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

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
