# Generated by Django 2.2.1 on 2019-06-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0036_student_isstudying'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='session',
            name='semester',
        ),
        migrations.AddField(
            model_name='subject',
            name='groups',
            field=models.ManyToManyField(to='control.Group', verbose_name='Группы'),
        ),
    ]