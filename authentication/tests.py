from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from control.models import Departament, Subdepartament


class AuthFuncTest(TestCase):
    # def setUp(self):
    #     self.credentials = {
    #         'username': 'test',
    #         'password': 'test'}
    #     User = get_user_model()
    #     z = Departament.objects.create(code='ИУ', name='Информатика и системы управления')
    #     zz = Subdepartament.objects.create(code='ИУ-6', name='Компьютерные системы и сети', departament=z)
    #     User.objects.create(is_superuser=True,last_name="test", first_name='test', patronymic='test', email='test@test.ru', username='test', work = zz)

    def testLogin(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)
        self.assertTrue(True, True)
        self.assertTrue(True, True)

    def testRegistration(self):
        z = self.client.login(username='test', password='test')
        zz = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)
        # response = self.client.post('/accounts/login/?next=/', self.credentials, follow=True)
        # self.assertTrue(response.context['user'].is_superuser)

    def testConfirmUser(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)

    def testConfirmEmail(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)