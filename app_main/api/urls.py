from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_main.api.viewsets import SubmissionCategoryViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'categories', SubmissionCategoryViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
