import time
import datetime
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from .models import RequestData


class RequestsModelTests(TestCase):

    def create_request_data(self):
        """
        Method for creating test data
        :return:
        """
        return RequestData.objects.create(http_request='/home/',
                                          remote_addr='127.0.0.1',
                                          date_time=datetime.datetime.now(),
                                          viewed=False)

    def test_requests_model_create_and_str(self):
        """
        Checked object string representation
        :return:
        """
        request_data = self.create_request_data()
        self.assertEqual(str(request_data), 'Request /home/ from 127.0.0.1')

    def test_requests_update(self):
        """
        Checked model to updating
        :return:
        """
        request_data = self.create_request_data()
        self.assertEqual(RequestData.objects.filter(viewed=True).count(), 0)
        request_data.viewed = True
        request_data.save()
        self.assertEqual(RequestData.objects.filter(viewed=True).count(), 1)

    def test_delete(self):
        """
        Checked model to deleting object
        :return:
        """
        request_data = self.create_request_data()
        self.assertEqual(RequestData.objects.all().count(), 1)
        request_data.delete()
        self.assertEqual(RequestData.objects.all().count(), 0)


class RequestsViewsMiddlewareTests(TestCase):

    def test_requests_middleware(self):
        """
        Checked requests middleware, make request and check it in the table
        :return:
        """
        client = Client()
        client.get('/')
        response = client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(RequestData.objects.count(), 0)

    def test_requests_index_page_context(self):
        """
        Checked requests index page context
        :return:
        """
        client = Client()
        client.get('/')
        response = client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['object_list'].count(), 0)

    def test_requests_index_json_data(self):
        """
        checked request context in index page
        :return:
        """
        client = Client()
        client.get('/')
        response = client.get(reverse('requests_data'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'requestsNew')

    def test_post_request_viewed(self):
        """
        checked post requests data
        :return:
        """
        client = Client()
        client.get('/')
        client.post(
            '/requests/requestsData/',
            {'data': json.dumps([{'request_id': 1}])},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(RequestData.objects.filter(viewed=True).count(), 1)

    def test_last_ten_requests(self):
        """
        Checked requests middleware, make request and check it in the table
        :return:
        """
        client = Client()
        requests_list = []
        for i in range(0, 15):
            time.sleep(1)
            client.get('/')
            requests_list.append({'time': datetime.datetime.now()})
        response = client.get(reverse('requests'))
        requests_from_context = [datetime.time(request.date_time.hour,
                                               request.date_time.minute,
                                               request.date_time.second)
                                 for request in
                                 response.context['object_list']]
        requests_from_db = [datetime.time(request.date_time.hour,
                                          request.date_time.minute,
                                          request.date_time.second)
                            for request in RequestData.objects.all().
                                               order_by('-date_time')[0:10]]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(requests_from_context), 10)
        self.assertEqual(requests_from_db, requests_from_context)
