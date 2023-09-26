# Generated by Django 4.2 on 2023-09-26 14:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import photo.storages_backend
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("description", models.TextField()),
                ("prize", models.TextField()),
                ("automated_dates", models.BooleanField(default=True)),
                (
                    "upload_phase_start",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("upload_phase_end", models.DateTimeField(blank=True, null=True)),
                ("voting_phase_end", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "picture_path",
                    models.FileField(
                        storage=photo.storages_backend.PublicMediaStorage(),
                        upload_to=photo.storages_backend.picture_path,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("email", models.TextField()),
                ("name_first", models.TextField(blank=True, null=True)),
                ("name_last", models.TextField(blank=True, null=True)),
                (
                    "profile_picture_updated_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("user_handle", models.TextField(null=True, unique=True)),
                (
                    "profile_picture",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_picture",
                        to="photo.picture",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PictureComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "picture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="photo.picture"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="photo.user"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="picture",
            name="likes",
            field=models.ManyToManyField(related_name="picture_likes", to="photo.user"),
        ),
        migrations.AddField(
            model_name="picture",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="picture_user",
                to="photo.user",
            ),
        ),
        migrations.CreateModel(
            name="ContestSubmission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("submission_date", models.DateTimeField(auto_now_add=True)),
                (
                    "contest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="photo.contest"
                    ),
                ),
                (
                    "picture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="photo.picture"
                    ),
                ),
                (
                    "votes",
                    models.ManyToManyField(
                        related_name="submission_votes", to="photo.user"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="contest",
            name="cover_picture",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="photo.picture",
            ),
        ),
        migrations.AddField(
            model_name="contest",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contest_created_by",
                to="photo.user",
            ),
        ),
        migrations.AddField(
            model_name="contest",
            name="winners",
            field=models.ManyToManyField(
                related_name="contest_winners", to="photo.user"
            ),
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "pictures",
                    models.ManyToManyField(
                        related_name="collection_pictures", to="photo.picture"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="photo.user"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="collection",
            constraint=models.UniqueConstraint(
                fields=("name", "user"), name="collection_pk"
            ),
        ),
    ]
