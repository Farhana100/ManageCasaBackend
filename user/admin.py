from django.contrib import admin
from .models import *


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number', 'num_of_apartments', 'num_of_tenants', 'service_charge_amount')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'bkash_acc_number')


class TenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'bkash_acc_number', 'arrival_date', 'departure_date')


admin.site.register(Building, BuildingAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Tenant, TenantAdmin)