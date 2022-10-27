# Generated by Django 4.1 on 2022-10-26 10:58

from django.db import migrations, models
import photo.models


class Migration(migrations.Migration):

    dependencies = [
        ("photo", "0003_comment_created_at_comment_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contest",
            name="updated_by",
            field=models.UUIDField(blank=True, null=True, verbose_name="updated by"),
        ),
        migrations.AlterField(
            model_name="submission",
            name="content",
            field=models.ImageField(
                blank=True, null=True, storage=photo.models.SubmissionContentStorage, upload_to=photo.models.upload_path
            ),
        ),
    ]
