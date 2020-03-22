from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserProfile, Transaction, CustomPackageRequest


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    contact_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'contact_number', 'password1', 'password2']


class UserUpdateForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class PurchaseForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['quantity']

    def clean_quantity(self, *args, **kwargs):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("You have entered an invalid quantity.")
        else:
            return quantity


class ProofOfPaymentForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['proof_of_payment']


class CustomPackageRequestForm(ModelForm):
    travel_inbound_flight_date = forms.DateField(
        label='Inbound Flight Date',
        widget=forms.DateInput(attrs={
            'type': 'date'
        }),
        required=False
    )
    travel_outbound_flight_date = forms.DateField(
        label='Outbound Flight Date',
        widget=forms.DateInput(attrs={
            'type': 'date'
        }),
        required=False
    )
    preferred_time = forms.TimeField(
        label='Preferred Time',
        help_text='We will contact you based on the time that you enter here.',
        widget=forms.TimeInput(attrs={
            'type': 'time'
        })
    )
    preferred_date = forms.DateField(
        label='Preferred Date',
        help_text='We will contact you based on the date that you enter here.',
        widget=forms.DateInput(attrs={
            'type': 'date'
        }),
        required=False
    )
    budget = forms.CharField(
        label='Budget for Entire Trip',
        help_text='Including accomodations, travel vouchers, etc. Not including flight tickets.'
    )
    hotel = forms.BooleanField(
        label='Hotel Accomodation',
        required=False
    )
    travel_voucher = forms.BooleanField(
        label='Travel Voucher',
        required=False
    )
    travel_insurance = forms.BooleanField(
        label='Travel Insurance',
        required=False
    )

    class Meta:
        model = CustomPackageRequest
        fields = [
            'budget',
            'quantity',
            'flight_ticket',
            'origin',
            'destination',
            'travel_outbound_flight_date',
            'travel_inbound_flight_date',
            'hotel',
            'travel_voucher',
            'travel_insurance',
            'additional_notes',
            'contact_person',
            'contact_number',
            'email_address',
            'preferred_date',
            'preferred_time'
        ]


