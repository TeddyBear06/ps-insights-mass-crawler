# Generated by Django 3.2.6 on 2021-08-08 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0011_batchurl_worker_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchurl',
            name='worker_group',
        ),
    ]
