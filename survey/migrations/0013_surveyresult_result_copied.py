# Generated by Django 2.2.10 on 2020-05-09 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0012_surveyresult_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresult',
            name='result_copied',
            field=models.BooleanField(default=False),
        ),
    ]
