# Generated by Django 2.2.10 on 2020-05-02 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0007_auto_20200502_0504'),
        ('settings', '0007_configuration_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='messages',
            field=models.ManyToManyField(blank=True, related_name='channels', to='message.Message'),
        ),
    ]