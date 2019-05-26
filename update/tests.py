from django.test import TestCase

# Create your tests here.
class UpdateFuncTest(TestCase):
    def testUpdate(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)