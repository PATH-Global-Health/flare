# Generated by Django 3.2.6 on 2021-08-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]