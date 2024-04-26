# Generated by Django 5.0.4 on 2024-04-17 22:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0002_profile_links_per_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='report_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='submission',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_main.submissioncategory'),
        ),
        migrations.AlterField(
            model_name='submissioncategory',
            name='name',
            field=models.CharField(default='brak kategorii', max_length=200),
        ),
    ]