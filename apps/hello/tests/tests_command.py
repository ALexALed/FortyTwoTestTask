from StringIO import StringIO
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from ..models import MyBio


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
        self.assertIn('[MyBio]', models_data)
        self.assertIn('[User]', models_data)
        models_data_list = models_data.split('\n')
        for model_row in models_data_list:
            if '[MyBio]' in model_row:
                self.assertEqual(model_row,
                                 '[MyBio] - {0} objects'.format(
                                     MyBio._default_manager.count())
                                 )
            if '[User]' in model_row:
                self.assertEqual(model_row,
                                 '[User] - {0} objects'.format(
                                     User._default_manager.count())
                                 )
