# Generated by Django 2.2.10 on 2020-05-03 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0008_channel_messages'),
        ('message', '0008_auto_20200503_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status_detail',
            field=models.ManyToManyField(blank=True, through='message.MessageStatus', to='settings.Configuration'),
        ),
        migrations.RemoveField(
            model_name='message',
            name='status',
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]