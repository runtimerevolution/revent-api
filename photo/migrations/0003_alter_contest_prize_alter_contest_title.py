# Generated by Django 4.2 on 2023-05-15 08:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("photo", "0002_alter_collection_pictures_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contest",
            name="prize",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="contest",
            name="title",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="collection",
            name="name",
            field=models.TextField(),
        ),
    ]
