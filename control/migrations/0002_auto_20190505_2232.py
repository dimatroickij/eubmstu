# Generated by Django 2.2 on 2019-05-05 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subdepartament',
            name='departament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.Departament', verbose_name='факультет'),
        ),
    ]
