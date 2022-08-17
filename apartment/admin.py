from django.contrib import admin
from .models import *


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('building', 'owner', 'tenant', 'floor_number', 'apartment_number', 'rent', 'service_charge_due_amount')


class ApartmentImageAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'image')


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage, ApartmentImageAdmin)
