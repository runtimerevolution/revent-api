# Generated by Django 4.2.5 on 2023-09-25 11:23

from django.db import migrations, models
import photo.storages_backend


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0008_alter_user_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picture",
            name="picture_path",
            field=models.FileField(
                storage=photo.storages_backend.PublicMediaStorage(),
                upload_to=photo.storages_backend.picture_path,
            ),
        ),
    ]
