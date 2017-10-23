from django.db import models
from django.conf import settings

from department.models import (
    Department,
    Employee)

from hostel.models import Floor, Block
from .utils import make_slug


class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='complaints')
    department = models.ForeignKey(Department, related_name='complaints')
    employee = models.ForeignKey(Employee, related_name='complaints')
    user_block = models.ForeignKey(Block, related_name='complaints')
    user_floor = models.ForeignKey(Floor, related_name='complaints')
    slug = models.SlugField(max_length=100, blank=True, primary_key=True)
    status = models.BooleanField(default=False)
    issue = models.BooleanField(default=False)
    # issue count -> number of times issue was raised for the same complaint
    issue_count = models.PositiveIntegerField(default=0)
    description = models.TextField()
    user_room = models.PositiveIntegerField(blank=True, null=True)  # here get the room number from user instance
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.department.name)

    # TODO replace this method with methods in the views that take parameters as per the room or floor complaint and save them accordingly
    def save(self, *args, **kwargs):
        self.user_room = self.user.room_no
        self.slug = make_slug(str(self.department.slug), str(self.user_block.slug), str(self.user_floor.floor_number), str(self.user.room_no))
        super(Complaint, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('slug', 'status'),
        )
        permissions = (
            ('view_his_complaints', 'Can View his own complaint'),
            ('change_his_complaints', 'Can change his own complaints'),
            ('delete_his_complaints', 'Can Delete his own complaints'),
            ('view_floor_complaints', 'Can view all complaints in the floor'),
            ('view_block_complaints', 'Can View all complaints in the Block'),
        )



# TODO
'''
If floor complaint -> slug = block-floor-dept(done)
if room complaint -> slug = block-floor-room-dept(done)
Assign the user
Assign the department
Assign an employee based on the complaint
assign the user_floor and the user_block by getting values from the user model
remove user room from the model and use it from the user model itself
'''

