# Generated by Django 3.2.12 on 2022-02-15 17:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dhis', '0012_auto_20220215_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dhis.instance'),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='version',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]