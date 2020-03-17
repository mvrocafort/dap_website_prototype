from django.contrib import admin
from .models import UserProfile, Package, Transaction

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Package)
admin.site.register(Transaction)
