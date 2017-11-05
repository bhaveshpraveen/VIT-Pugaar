from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Complaint
from .utils import inform_employee

@receiver(post_save, sender=Complaint)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # todo: add error handling in case the message wasn't sent, here or in inform_employee
        inform_employee(instance)
