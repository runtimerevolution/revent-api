# Generated by Django 4.2 on 2023-09-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.TextField(unique=True),
        ),
    ]