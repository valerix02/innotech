# Generated by Django 3.1.3 on 2020-11-28 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pallada_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrappeddata',
            name='data',
            field=models.JSONField(default={}, max_length=262144, verbose_name='User data'),
        ),
    ]
