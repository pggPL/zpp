from rest_framework import viewsets
from app_main.models import SubmissionCategory
from app_main.serializers import SubmissionCategorySerializer


class SubmissionCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubmissionCategory.objects.all()
    serializer_class = SubmissionCategorySerializer
