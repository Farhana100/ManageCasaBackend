from django.contrib import admin
from .models import *


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('building', 'company_name', 'address', 'phone_number', 'bkash_acc_number')


class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'title', 'fee', 'subscription_duration')


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'subscription_date', 'last_payment_date')


admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(ServicePackage, ServicePackageAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
