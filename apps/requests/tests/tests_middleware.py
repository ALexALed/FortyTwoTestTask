import json
from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.requests.models import RequestData


class RequestsMiddlewareTests(TestCase):

    def test_requests_middleware(self):
        """
        Checked requests middleware, make request and check it in the table
        :return:
        """
        self.client.get('/')
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RequestData.objects.count(), 2)

    def test_exclude_ajax_requests(self):
        """
        Checked to exclude ajax requests from middleware
        :return:
        """
        self.client.post(
            '/requests/requestsData/',
            {'data': json.dumps([{'request_id': 1, 'viewed': False}])},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(RequestData.objects.count(), 0)
