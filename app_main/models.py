from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Submission(models.Model):
    link = models.CharField(max_length=200)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
    category = models.ForeignKey("SubmissionCategory", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.platform.name + " - " + str(self.id)


class Platform(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubmissionCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Profile(AbstractUser):
    class RankChoices(models.TextChoices):
        JUNIOR = 'Junior', 'Junior'
        SENIOR = 'Senior', 'Senior'

    rank = models.CharField(
        max_length=10,
        choices=RankChoices.choices,
        default=RankChoices.JUNIOR,
    )
    
    def __str__(self):
        return self.username
    