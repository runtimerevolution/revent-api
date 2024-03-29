# Generated by Django 4.2.5 on 2023-11-29 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import photo.storages_backend
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("email", models.TextField(unique=True)),
                (
                    "username",
                    models.CharField(
                        max_length=150, null=True, verbose_name="username"
                    ),
                ),
                ("name_first", models.TextField(blank=True, null=True)),
                ("name_last", models.TextField(blank=True, null=True)),
                (
                    "profile_picture_updated_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("user_handle", models.TextField(null=True, unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
        ),
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
                ("is_deleted", models.BooleanField(default=False)),
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
            options={
                "abstract": False,
            },
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
                ("is_deleted", models.BooleanField(default=False)),
                ("name", models.TextField(blank=True, null=True)),
                (
                    "file",
                    models.ImageField(
                        storage=photo.storages_backend.PublicMediaStorage(),
                        upload_to=photo.storages_backend.picture_path,
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        related_name="picture_likes", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="picture_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
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
                ("is_deleted", models.BooleanField(default=False)),
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
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
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
                ("is_deleted", models.BooleanField(default=False)),
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
                        related_name="submission_votes", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
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
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contest",
            name="winners",
            field=models.ManyToManyField(
                related_name="contest_winners", to=settings.AUTH_USER_MODEL
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
                ("is_deleted", models.BooleanField(default=False)),
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
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_picture",
                to="photo.picture",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddConstraint(
            model_name="collection",
            constraint=models.UniqueConstraint(
                fields=("name", "user"), name="collection_pk"
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_deleted", "False")),
                fields=("email",),
                name="user_email",
            ),
        ),
    ]
