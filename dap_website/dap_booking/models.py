import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


def return_flight():
    return timezone.now() + timezone.timedelta(days=7)

class Package(models.Model):
    TAG_CHOICES = (
        ('New', 'New'),
        ('Hot', 'Hot'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=100)
    package_display_picture = models.ImageField(default='package_display_pictures/default_package_picture.jpg', upload_to='package_display_pictures')
    num_days = models.IntegerField()
    num_countries = models.IntegerField()
    num_cities = models.IntegerField()
    description = models.TextField(max_length=400)
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True, null=True)
    travel_outbound_flight_date = models.DateField(default=timezone.now)
    travel_inbound_flight_date = models.DateField(default=return_flight)

    inclusions = models.TextField(max_length=500)
    exclusions = models.TextField(max_length=500)
    terms_and_conditions = models.TextField(max_length=500)

    tag = models.CharField(choices=TAG_CHOICES, default='New', max_length=10, blank=True)

    def __str__(self):
        return self.title
