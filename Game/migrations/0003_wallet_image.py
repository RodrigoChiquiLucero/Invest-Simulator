# Generated by Django 2.1.2 on 2018-10-15 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Game', '0002_auto_20181013_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
