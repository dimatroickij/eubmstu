# Generated by Django 2.2.1 on 2019-05-12 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0026_auto_20190512_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name'], 'verbose_name': 'группа', 'verbose_name_plural': 'Группы'},
        ),
    ]