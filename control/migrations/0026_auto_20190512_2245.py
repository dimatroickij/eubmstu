# Generated by Django 2.2.1 on 2019-05-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0025_auto_20190512_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='isEmpty',
            field=models.BooleanField(default=False, verbose_name='Есть данные'),
        ),
    ]