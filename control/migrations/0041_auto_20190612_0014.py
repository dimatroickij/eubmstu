# Generated by Django 2.2.1 on 2019-06-11 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0040_auto_20190608_2308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['student'], 'verbose_name': 'Результаты сессии', 'verbose_name_plural': 'Результаты сессии'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name', 'first_name', 'patronymic'], 'verbose_name': 'студента', 'verbose_name_plural': 'Студенты'},
        ),
        migrations.AlterField(
            model_name='student',
            name='gradebook',
            field=models.CharField(max_length=15, verbose_name='Номер зачётной книжки'),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('first_name', 'last_name', 'patronymic', 'gradebook')},
        ),
    ]
