from django.shortcuts import render
from django.views.generic import ListView
from .models import Package


# Create your views here.
class PackageListView(ListView):
    model = Package
    template_name = 'dap_booking/home.html'
