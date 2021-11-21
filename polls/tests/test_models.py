from django.test import TestCase

from polls.models import Client


def add(a, b):
    return a + b


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(login=12456)

    def test_login_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('login').verbose_name
        self.assertEquals(field_label, 'ID пользователя')

    def test_str(self):
        client = Client.objects.first()
        expected_str = str(client.login)
        self.assertEquals(str(client), expected_str)

