# encoding: utf-8
import datetime
import json
from StringIO import StringIO
import os
from PIL import Image
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
        bio_object = self.create_my_bio_test_data()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "42 Coffee Cups Test Assignment")
        self.assertEqual(response.context['object'], bio_object)

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

    def test_bio_update_view(self):
        """
        Bio update view test
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('update', args=(bio_object.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], bio_object)

    def test_bio_update_data_form_valid_ajax(self):
        """
        Bio update view test ajax post data valid
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')

        resp = self.client.post(
            reverse('update', args=(bio_object.id,)),
            {'first_name': 'Ol',
             'last_name': 'Al',
             'birth_date': '1986-03-28',
             'photo': '',
             'email': 'alexaled@gmail.com',
             'jabber': 'alexaled1@khavr.com',
             'skype': 'alexaled',
             'other_contacts': 'alexaled@ukr.net',
             'biography': 'My bio'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(resp.status_code, 200)
        content_resp = json.loads(resp.content)
        updated_bio = MyBio.objects.get(pk=bio_object.id)
        self.assertEqual(content_resp['pk'], updated_bio.id)
        self.assertEqual(updated_bio.first_name, 'Ol')

    def test_bio_update_data_form_invalid_ajax(self):
        """
        Bio update view test ajax post data invalid
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')

        resp = self.client.post(
            reverse('update', args=(bio_object.id,)),
            {'first_name': '',
             'last_name': 'Al',
             'birth_date': '1986-03-28',
             'photo': '',
             'email': 'alexaled@gmail.com',
             'jabber': 'alexaled1@khavr.com',
             'skype': 'alexaled',
             'other_contacts': 'alexaled@ukr.net',
             'biography': 'My bio'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertNotEqual(resp.status_code, 200)
        content_resp = json.loads(resp.content)
        self.assertEqual(content_resp[u'first_name'][0],
                         u'This field is required.')

    def test_bio_update_data_form_valid(self):
        """
        Bio update view test post data valid
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')

        resp = self.client.post(
            reverse('update', args=(bio_object.id,)),
            {'first_name': 'Ol',
             'last_name': 'Al',
             'birth_date': '1986-03-28',
             'photo': '',
             'email': 'alexaled@gmail.com',
             'jabber': 'alexaled1@khavr.com',
             'skype': 'alexaled',
             'other_contacts': 'alexaled@ukr.net',
             'biography': 'My bio'},
        )
        self.assertEqual(resp.status_code, 302)
        updated_bio = MyBio.objects.get(pk=bio_object.id)
        self.assertEqual(updated_bio.first_name, 'Ol')

    def test_bio_update_data_form_invalid(self):
        """
        Bio update view test post data invalid
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')

        resp = self.client.post(
            reverse('update', args=(bio_object.id,)),
            {'first_name': '',
             'last_name': 'Al',
             'birth_date': '1986-03-28',
             'photo': '',
             'email': 'alexaled@gmail.com',
             'jabber': 'alexaled1@khavr.com',
             'skype': 'alexaled',
             'other_contacts': 'alexaled@ukr.net',
             'biography': 'My bio'},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form'].errors['first_name'][0],
                         u'This field is required.')

    def test_bio_update_data_photo(self):
        """
        Bio update view test post data valid with photo
        :return:
        """
        bio_object = self.create_my_bio_test_data()
        self.client.login(username='admin', password='admin')

        file_obj = StringIO()
        image = Image.new("RGBA", size=(700, 700), color=(256, 0, 0))
        image.save(file_obj, 'png')
        file_obj.name = 'test.png'
        file_obj.seek(0)

        resp = self.client.post(
            reverse('update', args=(bio_object.id,)),
            {'first_name': 'Ol',
             'last_name': 'Al',
             'birth_date': '1986-03-28',
             'photo': file_obj,
             'email': 'alexaled@gmail.com',
             'jabber': 'alexaled1@khavr.com',
             'skype': 'alexaled',
             'other_contacts': 'alexaled@ukr.net',
             'biography': 'My bio'},
        )
        self.assertEqual(resp.status_code, 302)
        updated_bio = MyBio.objects.get(pk=bio_object.id)
        self.assertEqual(updated_bio.first_name, 'Ol')
        self.assertEqual(updated_bio.photo.height, 200)
        self.assertEqual(updated_bio.photo.width, 200)
        try:
            file_image = updated_bio.photo.path
            os.remove(file_image)
        except Exception:
            print('Test image file not deleted!')
