# Generated by Django 3.2.12 on 2022-02-16 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhis', '0015_alter_section_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='period_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
