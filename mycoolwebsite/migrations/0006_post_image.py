# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycoolwebsite', '0005_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=1, upload_to=b'blogimage/'),
            preserve_default=False,
        ),
    ]