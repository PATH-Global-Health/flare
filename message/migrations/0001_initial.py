# Generated by Django 2.2.10 on 2020-05-14 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('content', models.TextField()),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('celery_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='MessageStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('success_count', models.IntegerField()),
                ('error_count', models.IntegerField()),
                ('config_error', models.BooleanField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
