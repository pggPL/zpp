# Generated by Django 5.0.4 on 2024-04-24 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0004_submission_was_exported'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissioncategory',
            name='is_null',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
