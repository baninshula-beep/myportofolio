from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from main.models import Education, Experience
from main.permissions import ExperiencePermission, IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import EducationSerializer, ExperienceSerializer


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


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list_create(request):
    """List/search Education records or create one for a superuser."""
    if request.method == "GET":
        # The serializer reads starred_by for each result; prefetching avoids
        # issuing an additional relation query for every Education row.
        educations = Education.objects.prefetch_related("starred_by").all()
        institution = request.query_params.get("institution", "").strip()
        if institution:
            educations = educations.filter(
                institution__icontains=institution
            )

        serializer = EducationSerializer(
            educations,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = EducationSerializer(
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    """Retrieve, update, or delete one Education record."""
    # Keep the related users available to calculated serializer fields without
    # a separate query for the detail representation.
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"),
        pk=education_id,
    )

    if request.method == "GET":
        serializer = EducationSerializer(
            education,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    """Toggle the authenticated user's star on an Education record."""
    with transaction.atomic():
        # On databases with row-level locking, this serializes concurrent
        # toggles so each request reads the preceding committed star state.
        education = get_object_or_404(
            Education.objects.select_for_update(),
            pk=education_id,
        )
        relation = education.starred_by
        if relation.filter(pk=request.user.pk).exists():
            relation.remove(request.user)
            is_starred = False
        else:
            relation.add(request.user)
            is_starred = True

        star_count = relation.count()

    return Response({
        "star_count": star_count,
        "is_starred": is_starred,
    })
