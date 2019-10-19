from django.test import TestCase
from api import models
# Easy to change user model in settings with get_user_model instead of User #
from django.contrib.auth import get_user_model


def sample_user(email='newuser@example.com', password='newusepass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTestCase(TestCase):
    """This class defines the test suite for the creditcard model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.mii = '3'
        self.mii_details = 'Travel and entertainment'
        user = sample_user()
        self.creditcard_number = '371559102252018'
        self.iin = self.creditcard_number[:6]
        self.iin_details = 'American Express'
        self.check_digit = '8'
        self.creditcard = models.Creditcard(
            ccnumber=self.creditcard_number,
            owner=user
        )

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'newuser2@example.com'
        password = 'newuserpass'
        user = sample_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'newuserunique@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'tester')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testerpass')

    def test_create_new_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'testsuper@example.com',
            'testpass'
        )

        self.assertTrue(user.is_superuser)

    def test_model_can_create_a_creditcard(self):
        """Test the creditcard model can create a creditcard."""
        old_count = models.Creditcard.objects.count()
        self.creditcard.save()
        new_count = models.Creditcard.objects.count()

        self.assertNotEqual(old_count, new_count)
