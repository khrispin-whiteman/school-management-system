# Generated by Django 2.2 on 2020-01-19 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20200117_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pupilattendance',
            name='course',
        ),
    ]
