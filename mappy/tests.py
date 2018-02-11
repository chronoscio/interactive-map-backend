from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Shape, State


class APITests(APITestCase):
    fixtures = ['france']
    @classmethod
    def setUpTestData(cls):
        cls.state_url = reverse('state-list')
        cls.shape_url = reverse('shape-list')

    def test_list_states(self):
        """
        Ensure the state api returns as expected
        """
        res = self.client.get(self.state_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), State.objects.count())

    def test_filter_states(self):
        """
        Ensure the date query_param is respected
        """
        res = self.client.get(self.state_url + '?date=999')
        self.assertEqual(len(res.json()), 0)
        res = self.client.get(self.state_url + '?date=1001')
        self.assertEqual(len(res.json()), 1)
