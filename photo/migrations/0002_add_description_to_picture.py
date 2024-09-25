from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]