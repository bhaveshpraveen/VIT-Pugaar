from django.db import models

from hostel.models import Block, Floor, Room, Toilet
from django.core.validators import RegexValidator
# TODO
"""
    Assign a user as the head of the Department
"""
class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return "{]".format(self.name)


class Cleaner(models.Model):
    department = models.ForeignKey(Department, related_name='cleaners')
    block = models.ForeignKey(Block, related_name='cleaners')
    floor = models.ForeignKey(Floor, related_name='cleaners')
    toilet = models.ForeignKey(Toilet, related_name='cleaners')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    id = models.AutoField()
    name = models.CharField(max_length=125)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    def __str__(self):
        return "{} works in {} and is currently assigned to {} block, {} floor".format(
            self.name.title(),
            self.department.name,
            self.block.name,
            self.floor.floor_number
        )



class Plumber(models.Model):
    pass

class Carpenter(models.Model):
    pass

class Electrician(models.Model):
    pass

class Painter(models.Model):
    pass
