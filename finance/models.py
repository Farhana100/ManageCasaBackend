from django.db import models

from serviceProvider.models import *
from user.models import *
from apartment.models import *


# Create your models here.

class Fund(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    paid_amount = models.FloatField(default=0, null=True)
    date = models.DateTimeField(default=0, null=True)
    transaction_no = models.CharField(max_length=30, null=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'fund'


class Expense(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    paid_amount = models.FloatField(default=0, null=True)
    date = models.DateTimeField(default=0, null=True)
    category = models.CharField(max_length=30, null=True)
    comment = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'expense'


# also store expense of users -> status: True
class Bill(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, null=True, on_delete=models.CASCADE, blank=True, help_text='null means service charge')
    package = models.ForeignKey(ServicePackage, null=True, on_delete=models.CASCADE, blank=True, help_text='null means service charge')
    payable_amount = models.FloatField(default=0, null=True)
    due_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.BooleanField(default=False, null=False, help_text='True: paid,False: unpaid')
    transaction_number = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'bill'
