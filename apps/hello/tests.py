import datetime
from django.test import TestCase
from django.test.client import Client
from hello.models import MyBio


class BioModelTests(TestCase):

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


class BioViewsTests(TestCase):
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

    def test_add_reception_view(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "42 Coffee Cups Test Assignment")
        self.assertEqual(response.context['object'].last_name, 'Aledinov')
