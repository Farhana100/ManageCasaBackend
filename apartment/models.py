from django.db import models
from user.models import *
from uuid import uuid4

def get_apartment_image_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/apartment_images/<filename>
    # file named by UUID
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'apartment_images/{0}'.format(filename)


class Apartment(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL)
    tenant = models.ForeignKey(Tenant, blank=True, null=True, on_delete=models.SET_NULL)
    floor_number = models.IntegerField(null=False)
    apartment_number = models.CharField(max_length=30, null=False)  # flatno. 4f
    rent = models.IntegerField(default=0, null=True)
    service_charge_due_amount = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.building) + '_' + self.apartment_number

    class Meta:
        db_table = 'apartment'


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_apartment_image_upload_path, null=True, blank=True)

    def __str__(self):
        return self.get_image()

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    class Meta:
        db_table = 'apartment_image'

