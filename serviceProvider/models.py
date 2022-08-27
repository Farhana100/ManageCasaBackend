from apartment.models import *


# Create your models here.

def get_service_provider_image_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/service_provider_images/<filename>
    # file named by UUID
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'service_provider_images/{0}'.format(filename)


class ServiceProvider(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=get_service_provider_image_upload_path, null=True, blank=True)
    phone_number = models.IntegerField(default=0, blank=True, null=True)
    bkash_acc_number = models.IntegerField(default=0)
    details = models.CharField(max_length=1000, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def __str__(self):
        return str(self.company_name)

    class Meta:
        db_table = 'service provider'


class ServicePackage(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    fee = models.FloatField(default=0, null=False)
    subscription_duration = models.FloatField(default=1, null=False, help_text='months')


class ApartmentSubscription(models.Model):
    apartment = models.ForeignKey(Apartment, null=False, on_delete=models.CASCADE)
    package = models.ForeignKey(ServicePackage, null=False, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(default=None, blank=True, null=True)
    last_payment_date = models.DateTimeField(default=None, blank=True, null=True)