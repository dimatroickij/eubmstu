# Generated by Django 2.2.2 on 2019-06-30 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0050_auto_20190629_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdepartament',
            name='prove',
            field=models.BooleanField(default=False),
        ),
    ]
