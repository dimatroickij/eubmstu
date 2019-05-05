from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=150, blank=True, help_text='Необязательное поле')
    AbstractUser._meta.get_field('first_name').blank = False
    AbstractUser._meta.get_field('first_name').help_text = 'Обязательное поле'
    AbstractUser._meta.get_field('last_name').blank = False
    AbstractUser._meta.get_field('last_name').help_text = 'Обязательное поле'
    class Meta(object):
        unique_together = ('email',)
