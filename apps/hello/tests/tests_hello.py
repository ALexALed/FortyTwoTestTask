# encoding: utf-8
import datetime
from django.contrib.auth.models import User
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.hello.models import MyBio


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
        self.assertEqual(MyBio.objects.count(), 0)
        self.create_my_bio_test_data()
        self.assertEqual(MyBio.objects.count(), 1)

    def test_update_doctor(self):
        """
        checked model to updating object
        :return:
        """
        bio = self.create_my_bio_test_data()
        bio.first_name = 'JJ'
        bio.save()
        bio_test = MyBio.objects.get(pk=1)
        self.assertEqual(str(bio_test), 'Bio data for JJ Aledinov')

    def test_delete(self):
        """
        checked model to deleting object
        :return:
        """
        self.assertEqual(MyBio.objects.count(), 0)
        self.create_my_bio_test_data()
        self.assertEqual(MyBio.objects.count(), 1)
        bio = MyBio.objects.get(pk=1)
        bio.delete()
        self.assertEqual(MyBio.objects.count(), 0)


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
        User.objects.create_superuser('admin', '', 'admin')

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
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)
        self.create_my_bio_test_data()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "42 Coffee Cups Test Assignment")
        self.assertEqual(response.context['object'].last_name, 'Aledinov')

    def test_index_view_cyrillic(self):
        """
        Cyrillic bio view test
        :return:
        """
        bio_object = self.create_my_bio_test_data(first_name=u'Алексей',
                                                  last_name=u'Алединов')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, bio_object.last_name)
        self.assertEqual(response.context['object'], bio_object)

    def test_without_entity_in_DB(self):
        """
        DB is empty test
        :return:
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_two_entities_in_DB(self):
        """
        Two entities stored in DB
        :return:
        """
        first_bio_object = self.create_my_bio_test_data()
        self.create_my_bio_test_data()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], first_bio_object)

    def test_bio_update(self):
        """
        Bio update view test
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('update', args=(bio_object.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], bio_object)