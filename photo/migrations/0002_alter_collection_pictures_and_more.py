# Generated by Django 4.2 on 2023-05-11 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="pictures",
            field=models.ManyToManyField(
                related_name="collection_pictures", to="photo.picture"
            ),
        ),
        migrations.AlterField(
            model_name="contestsubmission",
            name="votes",
            field=models.ManyToManyField(
                related_name="submission_votes", to="photo.user"
            ),
        ),
    ]