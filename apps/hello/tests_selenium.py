import datetime
from django.core import management
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from apps.hello.models import MyBio


class HelloIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(HelloIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(HelloIntegrationTests, cls).tearDownClass()

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

    def test_bio_update(self):
        """
        Check interactive login, index, update
        :return:
        """
        if MyBio.objects.count() == 0:
            self.create_my_bio_test_data()
        self.selenium.get('%s%s' % (self.live_server_url, reverse('login')))
        self.selenium.find_element_by_id('id_username').send_keys('admin')
        self.selenium.find_element_by_id('id_password').send_keys('admin')
        result = self.selenium.find_element_by_id('login')
        result.click()
        result = self.selenium.find_element_by_id('update')
        result.click()
        self.selenium.get('%s%s' % (self.live_server_url, reverse('update',
                                                                  args=(1,))))
        name_field = self.selenium.find_element_by_id('id_first_name')
        name_field.clear()
        name_field.send_keys('Aled')
        self.selenium.find_element_by_id('updateForm').submit()
        bio_object = MyBio.objects.first()
        self.assertEqual(bio_object.first_name, u'Aled')
