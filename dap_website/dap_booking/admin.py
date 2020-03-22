from django.contrib import admin
from .models import UserProfile, Package, Transaction, Passenger, CustomPackageRequest

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


admin.site.site_header = 'Discover Asia Philippines Admin'
admin.site.site_title = 'Discover Asia Philippines Admin'
admin.site.index_title = 'Discover Asia Philippines Administration'

class PassengerInline(admin.TabularInline):
    model = Passenger
    readonly_fields = (
        'last_name',
        'first_name', 'middle_initial', 'birthday',
        'gender', 'contact_number', 'email_address'
    )

    def has_add_permission(self, request):
        return False


class TransactionAdmin(admin.ModelAdmin):
    '''def proof_of_payment_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.proof_of_payment.url,
            width=obj.proof_of_payment.width,
            height=obj.proof_of_payment.height,
            )
        )'''
    list_display = (
        'user',
        'package',
        'id',
        'transaction_date',
        'proof_of_payment_status',
        'proof_of_payment_deadline',
        'is_overdue',
        'is_finished'

        #'total_price'
    )
    list_filter = (
        'transaction_date',
        'proof_of_payment_status',
        'is_overdue',
        'is_finished'
    )

    fields = (
        (
            'user',
            'transaction_date',
            'package',
            'quantity'
        ),

        (
            'proof_of_payment_deadline',
            'proof_of_payment',
            'proof_of_payment_status',
            'is_overdue'
        ),
        (
            'flight_ticket',
        ),
        'is_finished'
    )

    search_fields = (
        'package__title',
        'user__username'
    )

    inlines = [PassengerInline]

    '''def total_price(self, transaction):
        total = transaction.quantity * transaction.package.price
        return total'''


class PackageAdmin(admin.ModelAdmin):
    exclude = ('date_created',)
    list_display = (
        'title',
        'id',
        'date_created',
        'package_creator',
    )
    list_filter = (
        'package_creator',
        'date_created',
    )
    fields = (
        ('package_creator', 'title', 'package_display_picture'),
        ('num_days', 'num_countries', 'num_cities'),
        ('price', 'discounted_price'),
        ('travel_outbound_flight_date', 'travel_inbound_flight_date'),
        ('description', 'tag'),
        ('exclusions', 'inclusions'),
        'terms_and_conditions'
    )
    search_fields = (
        'title',
    )

    '''def save_model(self, request, obj, form, change):
        if not change:
            obj.package_creator = request.user
        obj.save()'''

class CustomPackageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'request_date',
        'flight_ticket',
        'hotel',
        'travel_voucher',
        'travel_insurance',
        'request_status'
    )
    fields = (
        ('request_date', 'user'),
        ('title', 'budget', 'quantity'),
        ('origin', 'destination'),
        ('flight_ticket', 'hotel', 'travel_voucher', 'travel_insurance', 'travel_outbound_flight_date', 'travel_inbound_flight_date'),
        'additional_notes',
        ('contact_person', 'contact_number', 'email_address', 'preferred_time'),
        'request_status'
    )

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Package, PackageAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Passenger)
admin.site.register(CustomPackageRequest, CustomPackageAdmin)
