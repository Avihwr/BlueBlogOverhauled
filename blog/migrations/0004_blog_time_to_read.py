# Generated by Django 3.1.2 on 2020-10-05 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201005_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='time_to_read',
            field=models.IntegerField(default=12),
        ),
    ]
