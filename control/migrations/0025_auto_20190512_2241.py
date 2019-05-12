# Generated by Django 2.2.1 on 2019-05-12 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0024_auto_20190512_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='isEmpty',
            field=models.BooleanField(default=True, verbose_name='Есть данные'),
        ),
        migrations.AddField(
            model_name='group',
            name='levelEducation',
            field=models.CharField(choices=[('bachelor', 'Бакалавриат'), ('magister', 'Магистратура'), ('specialist', 'Специалитет / Аспирантура')], max_length=10, null=True, verbose_name='Уровень образования'),
        ),
    ]
