# Generated by Django 2.2.1 on 2019-05-11 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0015_auto_20190512_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departament',
            name='number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]