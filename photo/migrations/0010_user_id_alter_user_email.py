# Generated by Django 4.2 on 2023-09-25 16:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0009_alter_picture_picture_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
