from django.db import models
from django.conf import settings

from department.models import (
    Department,
    Employee)

from hostel.models import Floor, Block

class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_complaints')
    department = models.ForeignKey(Department, related_name='department_complaints')
    employee = models.ForeignKey(Employee, related_name='employee_complaints')
    user_block = models.ForeignKey(Block, related_name='block_complaints')
    user_floor = models.ForeignKey(Floor, related_name='floor_complaints')
    slug = models.SlugField(max_length=100)
    status = models.BooleanField(default=False)
    issue = models.BooleanField(default=False)
    # issue count -> number of times issue was raised for the same complaint
    issue_count = models.PositiveIntegerField(default=0)
    description = models.TextField()
    user_room = models.PositiveIntegerField()  # here get the room number from user instance
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.department.name)

    class Meta:
        unique_together = (
            ('slug', 'status'),
        )



# TODO
'''
If floor complaint -> slug = block-floor-dept
if room complaint -> slug = block-floor-room-dept
remove user room from the model and use it from the user model itself
'''

