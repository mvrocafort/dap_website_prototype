from .models import Transaction, CustomPackageRequest


def unsettled_booking_count(request):
    count = Transaction.objects.filter(user__username=request.user.username, proof_of_payment_status=False).count()
    return {'unsettled_booking_count': count}


def pending_custom_package_request_count(request):
    #count = Transaction.objects.filter(user__username=request.user.username, proof_of_payment_status=False).count()
    count = CustomPackageRequest.objects.filter(user__username=request.user.username, request_status='Processing').count()
    return {'pending_custom_package_request_count': count}



#    pending_bookings = user.transaction_set.filter(proof_of_payment_status='PP').count()