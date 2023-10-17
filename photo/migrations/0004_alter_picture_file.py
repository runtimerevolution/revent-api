# Generated by Django 4.2.5 on 2023-10-11 15:09

from django.db import migrations, models
import photo.storages_backend


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0003_rename_picture_path_picture_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picture",
            name="file",
            field=models.ImageField(
                storage=photo.storages_backend.PublicMediaStorage(),
                upload_to=photo.storages_backend.picture_path,
            ),
        ),
    ]
