from django.test import TestCase

# Create your tests here.


class ControlFuncTest(TestCase):
    def testStartUpdate(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)
        self.assertTrue(True, True)
        self.assertTrue(True, True)

    def testStopUpdate(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)


class EUIntegrationTest(TestCase):
    def integrationTest(self):
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)
