# Generated by Django 4.2.3 on 2023-08-01 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_customuser_bio_remove_customuser_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
