from rest_framework import serializers
from app_main.models import Submission, Platform, SubmissionCategory, Profile


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']


class SubmissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionCategory
        fields = ['id', 'name', 'is_null']


class SubmissionSerializer(serializers.ModelSerializer):
    # Include nested serializers for related objects
    platform = PlatformSerializer(read_only=True)
    category = SubmissionCategorySerializer(read_only=True)
    # For writable nested fields, to let the client specify a change by ID
    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(), source='platform', write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SubmissionCategory.objects.all(), source='category', write_only=True, allow_null=True, required=False)

    class Meta:
        model = Submission
        fields = ['id', 'link', 'platform', 'platform_id', 'category', 'category_id', 'date',
                  'report_count', 'was_exported']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'rank', 'links_per_page', 'sorting']
        extra_kwargs = {
            'email': {'required': True},  # Assuming email should be required for a user profile
        }
