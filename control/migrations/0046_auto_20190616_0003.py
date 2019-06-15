# Generated by Django 2.2.2 on 2019-06-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0045_auto_20190615_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='type_rating',
            field=models.CharField(choices=[('Кур', 'Курсовая'), ('Зач', 'Зачёт'), ('Экз', 'Экзамен'), ('Прк', 'Практика'), ('РЭ', 'Рейтинговый экзамен'), ('НРС', 'НРС'), ('НИД', 'Научно-исследовательская деятельность')], max_length=5, verbose_name='Тип оценки'),
        ),
    ]