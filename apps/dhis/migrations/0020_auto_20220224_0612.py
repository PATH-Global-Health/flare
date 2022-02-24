# Generated by Django 3.2.12 on 2022-02-24 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dhis', '0019_auto_20220223_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datavalue',
            name='data_set',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='org_unit',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='period',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='status',
        ),
        migrations.RemoveField(
            model_name='datavalue',
            name='user',
        ),
        migrations.CreateModel(
            name='DataValueSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('period', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Synced', 'Synced')], default='Pending', max_length=8)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_datavalueset', to=settings.AUTH_USER_MODEL)),
                ('data_set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dhis.dataset')),
                ('org_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dhis.orgunit')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_datavalueset', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dhis.dhis2user')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
