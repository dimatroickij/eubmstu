# Generated by Django 2.2 on 2019-05-05 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_group_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(to='control.Student', verbose_name='Студенты'),
        ),
    ]