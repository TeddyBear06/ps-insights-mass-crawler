# Generated by Django 3.2.6 on 2021-08-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0009_auto_20210807_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchurl',
            name='cls',
            field=models.SmallIntegerField(help_text='Cumulative Layout Shift: Stabilité de la page', null=True),
        ),
        migrations.AlterField(
            model_name='batchurl',
            name='fid',
            field=models.SmallIntegerField(help_text='First Input Delay: Interactivité de la page (TBT in Lighthouse)', null=True),
        ),
        migrations.AlterField(
            model_name='batchurl',
            name='lcp',
            field=models.SmallIntegerField(help_text='Largest Contentful Paint: Performance de la page', null=True),
        ),
    ]
