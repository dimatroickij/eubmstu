# Generated by Django 2.2 on 2019-05-05 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20190505_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, help_text='Необязательное поле', max_length=150, verbose_name='Отчество'),
        ),
    ]