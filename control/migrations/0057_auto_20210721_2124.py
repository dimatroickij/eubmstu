# Generated by Django 3.2.4 on 2021-07-21 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0056_rename_guid_student_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='departament',
            name='isService',
            field=models.BooleanField(default=False, verbose_name='Служебный департамент'),
        ),
        migrations.AddField(
            model_name='subdepartament',
            name='isService',
            field=models.BooleanField(default=False, verbose_name='Служебная кафедра'),
        ),
    ]
