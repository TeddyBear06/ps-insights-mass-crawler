# Generated by Django 3.2.6 on 2021-08-07 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0008_pagespeedrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchurl',
            name='cls',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='batchurl',
            name='fid',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='batchurl',
            name='lcp',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='batchurl',
            name='performance',
            field=models.SmallIntegerField(null=True),
        ),
    ]
