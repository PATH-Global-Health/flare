# Generated by Django 2.2.10 on 2020-05-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_auto_20200510_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresult',
            name='result',
            field=models.TextField(null=True),
        ),
    ]