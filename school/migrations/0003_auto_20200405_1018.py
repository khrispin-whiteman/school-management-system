# Generated by Django 2.2 on 2020-04-05 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20200227_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='children',
            options={'verbose_name': 'Child', 'verbose_name_plural': 'Children'},
        ),
        migrations.AddField(
            model_name='course',
            name='courseUnit',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),0
    ]
