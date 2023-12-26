from django.contrib import admin

# Register your models here.

from .models import Submission, Platform, SubmissionCategory, Profile

admin.site.register(Submission)
admin.site.register(Platform)
admin.site.register(SubmissionCategory)
admin.site.register(Profile)