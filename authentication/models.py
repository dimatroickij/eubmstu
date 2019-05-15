from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


from control.models import Subdepartament


class User(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=150, blank=True, help_text='Необязательное поле')
    work = models.ForeignKey(Subdepartament, on_delete=models.CASCADE, verbose_name='Место работы')

    AbstractUser._meta.get_field('first_name').blank = False
    AbstractUser._meta.get_field('first_name').help_text = 'Обязательное поле'
    AbstractUser._meta.get_field('last_name').blank = False
    AbstractUser._meta.get_field('last_name').help_text = 'Обязательное поле'
    AbstractUser._meta.get_field('email').blank = False

    class Meta(object):
        unique_together = ('email',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

from authentication.tasks import sendEmailConnfirm
@receiver(post_save, sender=get_user_model())
def user_post_save(instance, created, *args, **kwargs):
    if created:
        sendEmailConnfirm(instance.pk)