# Generated by Django 3.2.4 on 2021-07-09 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0055_alter_session_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='guid',
            new_name='uuid',
        ),
    ]
