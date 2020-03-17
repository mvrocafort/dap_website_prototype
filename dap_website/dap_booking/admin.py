from django.contrib import admin
from .models import UserProfile, Package

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Package)
