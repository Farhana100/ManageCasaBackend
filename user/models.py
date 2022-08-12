from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from apartment.models import Apartment


def get_owner_image_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/owner_images/<filename>
    # file named by UUID
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'owner_images/{0}'.format(filename)


def get_tenant_image_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/tenant_images/<filename>
    # file named by UUID
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'tenant_images/{0}'.format(filename)



class Building(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.IntegerField(default=0)
    num_of_apartments = models.IntegerField(default=0)
    num_of_tenants = models.IntegerField(default=0)
    service_charge_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'building'


class Owner(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_owner_image_upload_path, null=True, blank=True)
    phone_number = models.IntegerField(default=0, blank=True, null=True)
    bkash_acc_number = models.IntegerField(default=0)
    
    

    def __str__(self):
        return self.user.username

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    class Meta:
        db_table = 'owner'


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_tenant_image_upload_path, null=True, blank=True)
    phone_number = models.IntegerField(default=0, blank=True, null=True)
    arrival_date = models.DateTimeField(default=None, blank=True, null=True)
    departure_date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    class Meta:
        db_table = 'tenant'
