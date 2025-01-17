import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pictures/default_profile_picture.jpg', upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = "User Profile"


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


def deadline():
    return timezone.now() + timezone.timedelta(days=14)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    transaction_date = models.DateTimeField(default=timezone.now)

    proof_of_payment = models.ImageField(blank=True, upload_to='proof_of_payment')
    proof_of_payment_deadline = models.DateTimeField(default=deadline)
    proof_of_payment_status = models.BooleanField('Verified', default=False)

    is_overdue = models.BooleanField('Overdue', default=False)
    is_finished = models.BooleanField('Finished', default=False)

    flight_ticket = models.FileField(blank=True, upload_to='flight_tickets')

    def getTotalPrice(self):
        if self.package.discounted_price:
            return self.package.discounted_price*self.quantity
        else:
            return self.package.price*self.quantity

    def __str__(self):
        return str(self.package)


class Passenger(models.Model):
    GENDER = (
        ('M', 'M'),
        ('F', 'F'),
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    last_name = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    middle_initial = models.CharField(max_length=5, blank=False)
    birthday = models.DateField(default=timezone.now, blank=False)
    gender = models.CharField(choices=GENDER, default='M', max_length=1, blank=False)
    contact_number = models.CharField(max_length=30, blank=False)
    email_address = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class CustomPackageRequest(models.Model):
    REQUEST_STATUS = (
        ('Approved', 'Approved'),
        ('Processing', 'Processing'),
    )
    BOOKING_STATUS = (
        ('Booked', 'Booked'),
        ('Pending', 'Pending'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=100, default='My Custom Package')
    budget = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)

    flight_ticket = models.BooleanField(default=False, blank=True)
    origin = models.CharField(max_length=100, blank=True)
    destination = models.CharField(max_length=100, blank=True)
    travel_outbound_flight_date = models.DateField(default=timezone.now)
    travel_inbound_flight_date = models.DateField(default=timezone.now)

    hotel_accomodation = models.BooleanField(default=False, blank=True)

    travel_voucher = models.BooleanField(default=False, blank=True)
    travel_insurance = models.BooleanField(default=False, blank=True)

    additional_notes = models.TextField(max_length=500, verbose_name='Additional Notes / Special Requests', blank=True)

    contact_person = models.CharField(max_length=100, blank=False)
    contact_number = models.CharField(max_length=30, blank=False)
    email_address = models.CharField(max_length=100, blank=False)
    preferred_date = models.DateField(default=timezone.now)
    preferred_time = models.TimeField(default=timezone.now)

    request_status = models.CharField(choices=REQUEST_STATUS, default='Processing', max_length=50)
    booking_status = models.CharField(choices=BOOKING_STATUS, default='Pending', max_length=50)

    def __str__(self):
        return self.title + " - " + str(self.id) + " - " + str(self.request_date)

    class Meta:
        verbose_name = "Custom Package Request"
