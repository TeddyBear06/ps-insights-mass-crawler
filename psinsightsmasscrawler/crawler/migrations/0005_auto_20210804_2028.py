# Generated by Django 3.2.6 on 2021-08-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0004_auto_20210804_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchurl',
            name='report',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='UrlReport',
        ),
    ]