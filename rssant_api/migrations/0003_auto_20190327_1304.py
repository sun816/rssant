# Generated by Django 2.1.7 on 2019-03-27 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssant_api', '0002_auto_20190317_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='content_hash_method',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='content_hash_value',
        ),
        migrations.RemoveField(
            model_name='rawfeed',
            name='content_hash_method',
        ),
        migrations.RemoveField(
            model_name='rawfeed',
            name='content_hash_value',
        ),
        migrations.AddField(
            model_name='feed',
            name='content_hash_base64',
            field=models.CharField(blank=True, help_text='base64 hash value of content', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rawfeed',
            name='content_hash_base64',
            field=models.CharField(blank=True, help_text='base64 hash value of content', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='content_hash_base64',
            field=models.CharField(blank=True, help_text='base64 hash value of content', max_length=200, null=True),
        ),
    ]
