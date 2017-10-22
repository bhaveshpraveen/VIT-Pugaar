from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin)

from hostel.models import Block, Floor

phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class MyUserManager(BaseUserManager):
    def create_user(self, registration_number, email, phone_number, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not registration_number:
            raise ValueError('Users must have an registration number')

        user = self.model(
            email=self.normalize_email(email),
            registration_number = registration_number,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, registration_number, email, phone_number, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            registration_number=registration_number,
            phone_number=phone_number
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    registration_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    room_no = models.IntegerField(blank=True, null=True)
    floor = models.ForeignKey(Floor, related_name='users', blank=True, null=True)
    block = models.ForeignKey(Block, related_name='users', blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def get_full_name(self):
        # The user is identified by their email address
        return "{} {} {}".format(
            self.first_name,
            self.middle_name,
            self.last_name
        )

    def get_short_name(self):
        return "{} {}".format(
            self.first_name,
            self.last_name
        )

    def __str__(self):
        return self.registration_number

    # django uses this method to check if a particular user is a super_user
    @property
    def is_superuser(self):
        return self.admin

    # django uses this method to check if a particular user is a staff
    @property
    def is_staff(self):
        return self.staff
