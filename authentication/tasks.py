from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authentication.views import TokenGenerator


def sendEmailConnfirm(userId):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=userId)
    mail_subject = 'Подтверждение Email на ЕУ'
    message = render_to_string('email/confirmEmail.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': TokenGenerator().make_token(user),
        'year': datetime.now()
    })
    email = EmailMultiAlternatives(
        mail_subject, message, to=[user.email],
    )
    email.attach_alternative(message, 'text/html')
    email.content_subtype = 'html'
    email.send()


def sendEmailNewUser(userId):
    UserModel = get_user_model()
    user = UserModel.objects.get(is_superuser=True)
    newUser = UserModel.objects.get(pk=userId)
    mail_subject = 'новый пользователь'
    message = render_to_string('email/newUserEmail.html', {
        'user': user,
        'newUser': newUser,
        'year': datetime.now()
    })
    email = EmailMultiAlternatives(
        mail_subject, message, to=[user.email],
    )
    email.attach_alternative(message, 'text/html')
    email.content_subtype = 'html'
    email.send()
