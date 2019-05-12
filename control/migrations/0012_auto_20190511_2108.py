# Generated by Django 2.2.1 on 2019-05-11 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0011_auto_20190505_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='code_current',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='code_session',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='name_current',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='name_session',
        ),
        migrations.AddField(
            model_name='semester',
            name='code',
            field=models.CharField(blank=True, max_length=7, unique=True, verbose_name='Код'),
        ),
        migrations.AddField(
            model_name='semester',
            name='current',
            field=models.BooleanField(default=True, verbose_name='Текущая успеваемость'),
        ),
        migrations.AddField(
            model_name='semester',
            name='name',
            field=models.CharField(default=True, max_length=40, unique=True, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='session',
            field=models.BooleanField(default=True, verbose_name='Сессия'),
        ),
    ]