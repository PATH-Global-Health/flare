# Generated by Django 3.2.19 on 2023-07-03 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dhis', '0003_auto_20221104_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataElementGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('data_element_group_id', models.CharField(max_length=40, unique=True)),
                ('version', models.UUIDField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_dataelementgroup', to=settings.AUTH_USER_MODEL)),
                ('data_element', models.ManyToManyField(to='dhis.DataElement')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhis.instance')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_dataelementgroup', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
