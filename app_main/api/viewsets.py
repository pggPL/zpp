from rest_framework import viewsets
from app_main.models import SubmissionCategory, Profile
from app_main.serializers import SubmissionCategorySerializer, ProfileSerializer

class SubmissionCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubmissionCategory.objects.all()
    serializer_class = SubmissionCategorySerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
