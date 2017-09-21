from django.core.validators import RegexValidator
from django.db import models


class DetailsMixin(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=125)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    class Meta:
        abstract = True
