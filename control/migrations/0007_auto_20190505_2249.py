# Generated by Django 2.2 on 2019-05-05 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0006_auto_20190505_2248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subdepartament',
            options={'ordering': ['code'], 'verbose_name': 'Кафедру', 'verbose_name_plural': 'Кафедры'},
        ),
    ]
