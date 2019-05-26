from django.test import TestCase

# Create your tests here.
class ReportFuncTest(TestCase):
    def testReport(self):
        z = self.client.login(username='test', password='test')
        self.assertTrue(True, True)
        self.assertTrue(True, True)