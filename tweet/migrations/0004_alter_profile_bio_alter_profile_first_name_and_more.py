# Generated by Django 5.0.7 on 2024-08-08 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0003_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
