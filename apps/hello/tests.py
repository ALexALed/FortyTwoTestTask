# encoding: utf-8
import datetime
from django.core import management
from django.test import TestCase
from django.test.client import Client
from hello.models import MyBio


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

    def create_my_bio_test_data(self):
        """
        Method for creating test data
        :return:
        """
        return MyBio.objects.create(first_name='Oleksii',
                                    last_name='Aledinov',
                                    birth_date=datetime.date.today(),
                                    biography='Info about me',
                                    email='alexaled@gmail.com',
                                    skype='alexaled',
                                    jabber='alexaled1@khavr.com',
                                    other_contacts='0968962750')

    def test_bio_model_str(self):
        """
        check object string representation
        :return:
        """
        bio = MyBio(first_name='Oleksii', last_name='Aledinov')
        self.assertEqual(str(bio), 'Bio data for Oleksii Aledinov')

    def test_create_bio(self):
        """
        checked model to creating object
        :return:
        """
        self.assertEqual(MyBio.objects.count(), 1)
        bio = self.create_my_bio_test_data()
        self.assertEqual(MyBio.objects.count(), 2)
        bio.delete()

    def test_update_doctor(self):
        """
        checked model to updating object
        :return:
        """
        bio = self.create_my_bio_test_data()
        bio.first_name = 'JJ'
        bio.save()
        bio_test = MyBio.objects.get(pk=2)
        self.assertEqual(str(bio_test), 'Bio data for JJ Aledinov')
        bio.delete()

    def test_delete(self):
        """
        checked model to deleting object
        :return:
        """
        self.assertEqual(MyBio.objects.count(), 1)
        self.create_my_bio_test_data()
        self.assertEqual(MyBio.objects.count(), 2)
        bio = MyBio.objects.get(pk=2)
        bio.delete()
        self.assertEqual(MyBio.objects.count(), 1)


class BioViewsTests(CleanTestCase):

    def setUp(self):
        """
        Avoid load initial fixtures
        :return:
        """
        management.call_command('flush',
                                load_initial_data=False,
                                verbosity=0,
                                interactive=False)

    def create_my_bio_test_data(self,
                                first_name='Oleksii',
                                last_name='Aledinov'):
        """
        Method for creating test data
        :return:
        """
        return MyBio.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    birth_date=datetime.date.today(),
                                    biography='Info about me',
                                    email='alexaled@gmail.com',
                                    skype='alexaled',
                                    jabber='alexaled1@khavr.com',
                                    other_contacts='0968962750')

    def test_index_view(self):
        """
        Bio view test
        :return:
        """
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "42 Coffee Cups Test Assignment")
        self.assertEqual(response.context['object'].last_name, 'Aledinov')

    def test_index_view_cyrillic(self):
        """
        Cyrillic bio view test
        :return:
        """
        client = Client()
        self.create_my_bio_test_data(first_name=u'Алексей',
                                     last_name=u'Алединов')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "42 Coffee Cups Test Assignment")
        self.assertEqual(response.context['object'].last_name,
                         u'Алединов')

    def test_without_entity_in_DB(self):
        """
        DB is empty test
        :return:
        """
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_two_entities_in_DB(self):
        """
        Two entities stored in DB
        :return:
        """
        self.create_my_bio_test_data()
        self.create_my_bio_test_data()
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 404)
