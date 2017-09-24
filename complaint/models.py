from django.db import models
from django.conf import settings

from department.models import (
    Department,
    Carpenter,
    Painter,
    Electrician,
    Cleaner,
    Plumber)

from hostel.models import Floor, Block

class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='complaints')
    department = models.ForeignKey(Department, related_name='complaints')
    status = models.BooleanField(default=False)
    description = models.TextField()
    user_block = models.ForeignKey(Block, related_name='complaints')
    user_floor = models.ForeignKey(Floor, related_name='complaints')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self):



