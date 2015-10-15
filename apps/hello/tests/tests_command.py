from StringIO import StringIO
from django.core.management import call_command
from django.test import TestCase


class TestShowModels(TestCase):
    def test_command(self):
        """
        Run command 'show_models' and check result
        :return:
        """
        content = StringIO()
        call_command('show_models', stdout=content)
        content.seek(0)
        models_data = content.read()
        self.assertEqual(True, '[MyBio]' in models_data)
        self.assertEqual(True, '[User]' in models_data)
