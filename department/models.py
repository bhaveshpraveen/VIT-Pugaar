from django.core.validators import RegexValidator
from django.db import models

from hostel.models import Block, Floor

# TODO
"""
    Assign a user as the head of the Department
"""

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return "{dep}".format(dep=self.name)


class Employee(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=125)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list
    department = models.ForeignKey(Department, related_name='dept_employees')
    block = models.ForeignKey(Block, related_name='block_employees')
    floor = models.ForeignKey(Floor, related_name='floor_employees', null=True)

    def __str__(self):
        return "{} of department {}".format(self.name, self.department)

