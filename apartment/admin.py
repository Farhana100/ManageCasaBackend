from django.contrib import admin
from .models import *


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('building', 'owner', 'tenant', 'floor_number', 'apartment_number', 'rent', 'service_charge_due_amount')


admin.site.register(Apartment, ApartmentAdmin)
