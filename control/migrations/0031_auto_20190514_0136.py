# Generated by Django 2.2.1 on 2019-05-13 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0030_auto_20190514_0134'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='group',
            index_together={('name', 'code', 'semester')},
        ),
    ]
