# Generated by Django 2.2.13 on 2020-07-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200724_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='look',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='阅读数'),
        ),
    ]
