from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User
from .models import DbSignals


class CleanTestCase(TestCase):
    def setUp(self):
        """
        Avoid load initial fixtures
        :return:
        """
        management.call_command('flush',
                                load_initial_data=False,
                                verbosity=0,
                                interactive=False)


class BioModelTests(CleanTestCase):

    def create_user_test_data(self):
        """
        Method for creating test data
        :return:
        """
        return User.objects.create_user(username='Example',
                                        email='example@example.com',
                                        password='111111')

    def test_save_signal(self):
        """
        checked model to creating object
        :return:
        """
        pre_save = DbSignals.objects.filter(signal='save').count()
        self.create_user_test_data()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(pre_save + 1,
                         DbSignals.objects.filter(signal='save').count())

    def test_init_signal(self):
        """
        checked model to init object
        :return:
        """
        pre_count = DbSignals.objects.filter(signal='init').count()
        User(username='Example',
             email='example@example.com',
             password='111111')
        self.assertEqual(pre_count + 1,
                         DbSignals.objects.filter(signal='init').count())

    def test_delete_signal(self):
        """
        checked model to delete object
        :return:
        """
        user = self.create_user_test_data()
        self.assertEqual(User.objects.count(), 1)
        user.delete()
        self.assertEqual(DbSignals.objects.filter(signal='delete').count(), 1)
