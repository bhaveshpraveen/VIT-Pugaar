from django.db import models

from hostel.models import Block, Floor
from .utils import DetailsMixin


# TODO
"""
    Assign a user as the head of the Department
"""

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return "{dep}".format(dep=self.name)


class Cleaner(DetailsMixin):
    department = models.ForeignKey(Department, related_name='cleaners')
    block = models.ForeignKey(Block, related_name='cleaners')
    floor = models.ForeignKey(Floor, related_name='cleaners')
    # toilet = models.ForeignKey(Toilet, related_name='cleaners')


    def __str__(self):
        return "{} works in {} department and is currently assigned to {} block in floor {}".format(
            self.name.title(),
            self.department.name,
            self.block.name,
            self.floor.floor_number
        )



class Plumber(DetailsMixin):
    department = models.ForeignKey(Department, related_name='plumbers')
    block = models.ForeignKey(Block, related_name='plumbers')

    def __str__(self):
        return "Plumber: {} belongs to {} department".format(self.name, self.department.name)


class Carpenter(DetailsMixin):
    department = models.ForeignKey(Department, related_name='carpenters')
    block = models.ForeignKey(Block, related_name='carpenters')

    def __str__(self):
        return "Carpenter: {} belongs to {} department".format(self.name, self.department.name)


class Electrician(DetailsMixin):
    department = models.ForeignKey(Department, related_name='electricians')
    block = models.ForeignKey(Block, related_name='electricians')

    def __str__(self):
        return "Electrician: {} belongs to {} department".format(self.name, self.department.name)


class Painter(DetailsMixin):
    department = models.ForeignKey(Department, related_name='painters')
    block = models.ForeignKey(Block, related_name='painters')

    def __str__(self):
        return "Painter: {} belongs to {} department".format(self.name, self.department.name)
