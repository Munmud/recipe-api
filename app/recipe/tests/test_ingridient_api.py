from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingridient

from recipe.serializers import IngridientSerializer

INGRIDIENT_URL = reverse('recipe:ingridient-list')


class PublicIngridientApiTests(TestCase):
    """Publicly availabel Ingridient API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGRIDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngridientApiTests(TestCase):
    """Test the Private Ingridient that can be retrive by authorised user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@munmud.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingridient_list(self):
        """Test retriving a list of ingridient"""
        Ingridient.objects.create(user=self.user, name='mosla')
        Ingridient.objects.create(user=self.user, name='salt')

        res = self.client.get(INGRIDIENT_URL)
        Ingridients = Ingridient.objects.all().order_by('-name')
        serializer = IngridientSerializer(Ingridients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridient_limited_to_user(self):
        """Test that ingridents for the authenticated user only"""
        user2 = get_user_model().objects.create_user(
            'test2@munmud.com',
            'testpass1234',
        )
        Ingridient.objects.create(user=user2, name='mosla')
        ingridient = Ingridient.objects.create(user=self.user, name='salt')

        res = self.client.get(INGRIDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingridient.name)

    def test_create_ingridient_successful(self):
        """Test Creating a new Ingridient"""
        payload = {'name': 'Test Ingridient'}
        self.client.post(INGRIDIENT_URL, payload)

        exist = Ingridient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exist)

    def test_create_ingridient_invalid(self):
        """Test creating a new ingridient with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(INGRIDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
