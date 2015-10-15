import datetime
from django.template import Context, Template
from ..models import MyBio
from .tests_hello_models import CleanTestCase


class TestEditLink(CleanTestCase):

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

    def test_create_admin_link(self):
        """
        checked to creating admin link
        :return:
        """
        object_bio = self.create_my_bio_test_data()
        template = Template("{% load edit_link %}{% edit_link object %}")
        context = Context()
        context["object"] = object_bio
        rendered = template.render(context)
        self.assertEqual(u"/admin/hello/mybio/{0}/".format(object_bio.id),
                         rendered)
        response = self.client.get(rendered)
        self.assertEqual(response.status_code, 200)
