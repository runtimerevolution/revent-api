# Generated by Django 4.1 on 2022-10-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photo", "0004_alter_contest_updated_by_alter_submission_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="content",
            field=models.TextField(default="default_content"),
            preserve_default=False,
        ),
    ]
