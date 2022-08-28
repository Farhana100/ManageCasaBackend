from django.contrib import admin
from .models import *


# Register your models here.
class FundAdmin(admin.ModelAdmin):
    list_display = ('building', 'owner', 'paid_amount', 'date', 'transaction_no')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('building', 'paid_amount', 'date', 'category', 'comment')


class BillAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'service_provider', 'payable_amount', 'due_date', 'payment_date', 'status', 'transaction_number',
        'description')


admin.site.register(Fund, FundAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Bill, BillAdmin)
