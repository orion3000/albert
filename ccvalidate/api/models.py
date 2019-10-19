from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User email address must not be blank')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # allow for various db types
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username
    because everyone has an email.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Creditcard(models.Model):
    """This class represents the creditcard model."""
    ccnumber = models.CharField(
        validators=[MinLengthValidator(15)],
        max_length=19,
        blank=False,
        unique=False
    )
    mii = models.CharField(
        validators=[MinLengthValidator(1)],
        max_length=1,
        blank=True,
        unique=False
    )
    mii_details = models.CharField(max_length=255, blank=True, unique=False)
    iin = models.CharField(
        validators=[MinLengthValidator(6)],
        max_length=6,
        blank=True,
        unique=False
    )
    # Could create an Issuer class and use a ForeignKey if list was longer#
    iin_details = models.CharField(max_length=32, blank=True, unique=False)
    pan = models.CharField(
        validators=[MinLengthValidator(6)],
        max_length=12,
        blank=True,
        unique=False
    )
    network = models.CharField(max_length=32, blank=True, unique=False)
    check_digit = models.CharField(
        validators=[MinLengthValidator(1)],
        max_length=1,
        blank=True,
        unique=False
    )
    valid = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'api.User',
        related_name='creditcards',
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Return a human readable representation of model instance"""
        return "{}".format(self.ccnumber)
