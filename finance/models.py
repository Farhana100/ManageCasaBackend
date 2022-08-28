from django.db import models
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