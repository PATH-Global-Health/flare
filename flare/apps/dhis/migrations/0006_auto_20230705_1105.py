# Generated by Django 3.2.20 on 2023-07-05 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dhis', '0005_dataelementgroupset'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataElementGroupGroupSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('version', models.UUIDField(default=uuid.uuid4)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_dataelementgroupgroupset', to=settings.AUTH_USER_MODEL)),
                ('data_element_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhis.dataelementgroup')),
                ('data_element_groupset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhis.dataelementgroupset')),
                ('instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dhis.instance')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_dataelementgroupgroupset', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
        migrations.AddField(
            model_name='dataelementgroupset',
            name='data_element_groups',
            field=models.ManyToManyField(through='dhis.DataElementGroupGroupSet', to='dhis.DataElementGroup'),
        ),
    ]