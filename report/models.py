from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Report(models.Model):
    name = models.CharField('Название отчёта', max_length=200)
    settings = models.CharField('Параметры отчёта', max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField('Дата создания отчёта')
    link = models.CharField('Ссылка для скачивания отчёта', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['date']