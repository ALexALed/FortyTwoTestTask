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

    def test_create_save_signal(self):
        """
        checked model to creating and save object
        :return:
        """
        pre_save = DbSignals.objects.filter(signal='create').count()
        user = self.create_user_test_data()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(pre_save + 1,
                         DbSignals.objects.filter(signal='create').count())

        pre_save = DbSignals.objects.filter(signal='save').count()
        user.save()
        self.assertEqual(pre_save + 1,
                         DbSignals.objects.filter(signal='save').count())

    def test_delete_signal(self):
        """
        checked model to delete object
        :return:
        """
        user = self.create_user_test_data()
        self.assertEqual(User.objects.count(), 1)
        user.delete()
        self.assertEqual(DbSignals.objects.filter(signal='delete').count(), 1)
