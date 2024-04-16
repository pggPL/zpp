from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_main.api.viewsets import SubmissionCategoryViewSet

router = DefaultRouter()
router.register(r'categories', SubmissionCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
