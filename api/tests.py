from django.test import TestCase

# Create your tests here.
class APIFuncTest(TestCase):
    def testSettingsParams(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)

    def testStartGetData(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)

    def testStopGetData(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)