from django.db import models
from user.models import *


class Apartment(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL)
    tenant = models.ForeignKey(Tenant, blank=True, null=True, on_delete=models.SET_NULL)
    floor_number = models.IntegerField(null=False)
    apartment_number = models.CharField(max_length=30, null=False)  # flatno. 4f
    rent = models.IntegerField(default=0, null=True)
    service_charge_due_amount = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.apartment_number

    class Meta:
        db_table = 'apartment'
