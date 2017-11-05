from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify

from hostel.models import Block, Floor

# TODO
"""
    Assign a user as the head of the Department
"""


class Department(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, primary_key=True)

    def __str__(self):
        return "{dep}".format(dep=self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)


class Employee(models.Model):
    phone_regex = RegexValidator(regex=r'^\d{10}$',
                                 message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")

    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=125)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list
    department = models.ForeignKey(Department, related_name='employees')
    block = models.ForeignKey(Block, related_name='employees')
    floor = models.ForeignKey(Floor, related_name='employees', null=True, blank=True)

    def __str__(self):
        return "{} of department {}".format(self.name, self.department)

