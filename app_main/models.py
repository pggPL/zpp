from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Submission(models.Model):
    link = models.CharField(max_length=200)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
    category = models.ForeignKey("SubmissionCategory", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    report_count = models.IntegerField(default=1)

    # indicates if the submission was exported after filling the category
    was_exported = models.BooleanField(default=False)

    def __str__(self):
        return self.platform.name + " - " + str(self.id)

class ProfileSubmission(models.Model):
    link = models.CharField(max_length=200)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.platform.name + " - " + str(self.id)

class Platform(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubmissionCategory(models.Model):
    name = models.CharField(max_length=200, default="brak kategorii")

    # This field (if true) tells that the category indicates "no category given"
    is_null = models.BooleanField()

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

    links_per_page = models.IntegerField(default=10)

    sorting = models.CharField(max_length=40, default='by_date')

    def get_links_per_page(self):
        return self.links_per_page

    def set_links_per_page(self, links_per_page):
        self.links_per_page = links_per_page
        self.save()
    
    def __str__(self):
        return self.username

