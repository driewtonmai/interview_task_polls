from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse

from polls.models import Poll


class TestActivePollView(TestCase):
    # def setUp(self):
    #     self.poll = Poll.objects.create()

    def test_list_GET(self):
        response = self.client.get(reverse('polls:polls-active-list'))
        self.assertEquals(response.status_code, 200)

    def test_detail_GET(self):
        response = self.client.get(reverse('polls:polls-detail', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 200)

    # def test_detail_GET_404(self):
    #     response = self.client.get(reverse('polls:polls-detail', kwargs={'pk': 0}))
    #     self.assertEquals(response.status_code, 404)
