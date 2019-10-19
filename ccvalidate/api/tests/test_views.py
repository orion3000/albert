from django.test import TestCase
from api import models
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        email = 'newuser@example.com'
        password = 'newuserpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.creditcard_data = {'ccnumber': '371559102252018',
                                'owner': user.id
                                }
        self.response = self.client.post(
            reverse('create'),
            self.creditcard_data,
            format="json"
        )
        self.creditcard_valid_data = {'ccnumber': '371559102252018'}
        self.valid_response_body = '{"ccnumber": "371559102252018", ' \
            '"valid": true, "mii": "3", "mii_details": "Banking & ' \
            'Financial (Visa, Switch, and Electron)", "iin": "371559' \
            '", "iin_details": "American Express", "pan": "10225201"' \
            ', "network": "American Express", "check_digit": "8"}'
        self.creditcard_invalid_data = {'ccnumber': '371559102252018a'}
        self.invalid_response_body = '{"Error": "Credit card number is ' \
                                     'not only digits."}'
        self.creditcard_short_data = {'ccnumber': '37155910'}
        self.short_response_body = '{"Error": "Credit card number is not ' \
                                   'enough digits."}'
        self.creditcard_long_data = {'ccnumber': '37155910225201899999999'}
        self.long_response_body = '{"Error": "Credit card number is too ' \
                                  'many digits."}'
        self.network_valid_data = {'network': 'Visa'}
        self.network_invalid_data = {'network': 'Misa'}

    def test_api_can_create_user_with_email(self):
        """"Test creating a new user with an email is successful"""
        email = 'newuser2@example.com'
        password = 'newuserpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_api_can_create_a_creditcard(self):
        """Test the api has creditcard creation capability."""

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get(
            '/creditcard/1/',
            kwargs={'pk': 3},
            format="json"
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_get_a_creditcard(self):
        """Test the api can get a given creditcard."""
        creditcard = models.Creditcard.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': creditcard.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, creditcard)

    def test_api_can_update_creditcard(self):
        """Test the api can update a given creditcard."""
        creditcard = models.Creditcard.objects.get()
        change_creditcard = {"ccnumber": "371559102252018"}
        response = self.client.put(
            reverse('details', kwargs={'pk': creditcard.id}),
            change_creditcard, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_creditcard(self):
        """Test the api can delete a creditcard."""
        creditcard = models.Creditcard.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': creditcard.id}),
            format='json',
            follow=True
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_validate_a_creditcard(self):
        """Test the api has validatecard capability."""
        self.response = self.client.post(
            reverse('validate'),
            self.creditcard_valid_data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.response.content,
            self.valid_response_body.encode('utf-8')
        )

    def test_api_can_error_on_bad_creditcard_digits(self):
        """Test the api method validate returns proper bad digits error
         response."""
        self.response = self.client.post(
            reverse('validate'),
            self.creditcard_invalid_data,
            format="json"
        )

        self.assertEqual(
            self.response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            self.response.content,
            self.invalid_response_body.encode('utf-8')
        )

    def test_api_can_error_on_short_creditcard(self):
        """Test the api method validate returns proper not enough digits
        error response."""
        self.response = self.client.post(
            reverse('validate'),
            self.creditcard_short_data,
            format="json"
        )

        self.assertEqual(
            self.response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            self.response.content,
            self.short_response_body.encode('utf-8')
        )

    def test_api_can_error_on_long_creditcard(self):
        """Test the api method validate returns proper too many digits
        error response."""
        self.response = self.client.post(
            reverse('validate'),
            self.creditcard_long_data,
            format="json"
        )

        self.assertEqual(
            self.response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            self.response.content,
            self.long_response_body.encode('utf-8')
        )

    def test_api_can_generate_a_creditcard(self):
        """Test the api has gencard capability."""
        self.response = self.client.post(
            reverse('generate'),
            self.network_valid_data,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_api_can_error_on_invalid_network(self):
        """Test the api errors when the network is invalid for gencard."""
        self.response = self.client.post(
            reverse('generate'),
            self.network_invalid_data,
            format="json"
        )

        self.assertEqual(
            self.response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
