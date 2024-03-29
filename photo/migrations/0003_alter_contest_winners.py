# Generated by Django 4.2.8 on 2023-12-07 17:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0002_contest_internal_status_contest_voting_draw_end"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contest",
            name="winners",
            field=models.ManyToManyField(
                blank=True, related_name="contest_winners", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
