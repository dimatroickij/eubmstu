# Generated by Django 2.2.2 on 2019-06-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0042_auto_20190615_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='point',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество баллов за предмет'),
        ),
        migrations.AlterField(
            model_name='session',
            name='rating',
            field=models.CharField(blank=True, choices=[('Зчт', 'Зачтено'), ('Нзч', 'Не зачтено'), ('Отл', 'Отлично'), ('Хор', 'Хорошо'), ('Удов', 'Удовлетворительно'), ('НА', 'Не аттестован'), ('Я', 'Неявка')], max_length=4, null=True, verbose_name='Оценка'),
        ),
    ]
