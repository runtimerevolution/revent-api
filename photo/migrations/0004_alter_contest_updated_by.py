# Generated by Django 4.1 on 2022-11-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photo", "0003_comment_created_at_comment_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contest",
            name="updated_by",
            field=models.UUIDField(null=True, verbose_name="updated by"),
        ),
    ]
