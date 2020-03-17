from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Transaction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    contact_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'contact_number', 'password1', 'password2']


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
