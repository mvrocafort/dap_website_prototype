import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import inlineformset_factory, DateInput
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.conf import settings
from .models import Package, Transaction, Passenger, CustomPackageRequest
from .forms import (
    UserRegisterForm,
    UserProfileUpdateForm,
    UserUpdateForm,
    PurchaseForm,
    ProofOfPaymentForm,
    CustomPackageRequestForm
)


# Create your views here.
# We set the variable quantity as a global quantity so that we can
# pass the quantity entered by the user from the purchase form to
# the passenger form. The quantity will dictate the number of
# formsets to be filled by the user in the passenger details
quantity = "0"


def login(request):
    return render(request, 'dap_booking/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Account created for {username} successful! You can now log in using the credentials that you entered.')
            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            subject = f'Welcome to Discover Asia Philippines'
            message = f'Thank you for joining our Discover Asia Philippines family. You can now book any available package from the offered packages and even customize your own!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [form.cleaned_data['email'], 'mrocafort20@gmail.com']
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            return redirect('dap_booking:login')
    else:
        form = UserRegisterForm()
    return render(request, 'dap_booking/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dap_booking:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'dap_booking/profile.html', context)


class PackageListView(ListView):
    model = Package
    template_name = 'dap_booking/home.html'
    context_object_name = 'packages'
    ordering = ['-date_created']  # display the latest package created on top


class PackageDetailView(DetailView):
    model = Package
    template_name = 'dap_booking/package.html'


@login_required
def purchase(request, pk):
    package = Package.objects.get(pk=pk)
    user = User.objects.get(username=request.user.username)
    form = PurchaseForm(initial={'package': package, 'user': user})
    if request.method == 'POST':
        form = PurchaseForm(request.POST, initial={'package': package, 'user': user})
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.package = package
            post.proof_of_payment_status = False
            post.save()
            global quantity
            quantity = post.quantity
            return redirect('dap_booking:passenger_details', post.id)

    context = {'form': form, 'package': package}
    return render(request, 'dap_booking/purchase_form.html', context)


@login_required
def passenger_details(request, pk):
    PassengerFormSet = inlineformset_factory(Transaction, Passenger, fields=('last_name',
                                                                             'first_name', 'middle_initial', 'birthday',
                                                                             'gender', 'contact_number', 'email_address'), widgets={'birthday': DateInput(attrs={'type': 'date'})}, extra=quantity)
    transaction = Transaction.objects.get(id=pk)
    formset = PassengerFormSet(queryset=Passenger.objects.none(), instance=transaction)

    if request.method == 'POST':
        formset = PassengerFormSet(request.POST, instance=transaction)
        if formset.is_valid():
            formset.save()
            messages.success(request, f'Your booking details have been saved. Please settle your payment before {transaction.proof_of_payment_deadline} to avoid conflicts.')
            return redirect('dap_booking:transaction_details', transaction.id)
    context = {'form': formset, 'quantity': quantity}
    return render(request, 'dap_booking/passenger_form.html', context)


@login_required
def transaction_details(request, pk):
    transaction = Transaction.objects.get(id=pk)
    passengers = transaction.passenger_set.all()

    if request.method == 'POST':
        form = ProofOfPaymentForm(request.POST,
                                       request.FILES,
                                       instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your proof of payment has been uploaded!')
            return redirect('dap_booking:transaction_details', transaction.id)

    else:
        form = ProofOfPaymentForm(instance=transaction)
    context = {'passengers': passengers, 'transaction': transaction, 'form': form}
    return render(request, 'dap_booking/transaction_details.html', context)


@login_required
def bookings(request, pk):
    user = User.objects.get(id=pk)
    bookings = user.transaction_set.all().order_by('proof_of_payment_status')
    #custom_packages = user.custompackagerequest_set.all().order_by('-request_date')

    context = {
        'user': user,
        'bookings': bookings,
        #'custom_packages': custom_packages,
    }
    return render(request, 'dap_booking/bookings.html', context)


@login_required
def custom_package_request(request):
    user = User.objects.get(username=request.user.username)
    form = CustomPackageRequestForm(initial={'user': user})

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = CustomPackageRequestForm(request.POST, initial={'user': user})
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            subject = f'Discover Asia Philippines'
            message = f'Your custom package has been saved. Details: {post.origin} to {post.destination}.'
            from_email = settings.EMAIL_HOST_USER
            to_list = ['mrocafort20@gmail.com', form.cleaned_data['email_address']]
            #send_mail(subject, message, from_email, to_list, fail_silently=False)

            messages.success(request, f'Package Request has been sent to the admin. Please wait for an email.')
            return redirect('/')

    context = {'form': form}
    return render(request, 'dap_booking/custom_package_form.html', context)


@login_required
def custom_package_request_bookings(request, pk):
    user = User.objects.get(id=pk)
    custom_packages = user.custompackagerequest_set.all().order_by('-request_date')
    print(CustomPackageRequest.objects.filter(user__username=request.user.username, request_status='Pending').count())
    context = {
        'user': user,
        'custom_packages': custom_packages,
    }
    return render(request, 'dap_booking/custom_package_requests.html', context)


@login_required
def custom_package_request_details(request, pk):
    custom_package = CustomPackageRequest.objects.get(id=pk)
    
    context = {'custom_package': custom_package}
    return render(request, 'dap_booking/custom_package_details.html', context)


def dashboard(request):
    labels = []
    data = []

    package_trend = Package.objects.all()
    for x in package_trend:
        labels.append(x.title)
        data.append(x.transaction_set.count())

    #print(package_trend)

    pending_bookings = Transaction.objects.filter(proof_of_payment_status=False).count()
    finished_bookings = Transaction.objects.filter(is_finished=True).count()
    pending_custom_package_requests = CustomPackageRequest.objects.filter(request_status='Approved').count()
    finished_custom_package_requests = CustomPackageRequest.objects.filter(request_status='Processing').count()

    context = {
        'labels': labels,
        'data': data,
        'pending_bookings': pending_bookings,
        'finished_bookings': finished_bookings,
        'pending_custom_package_requests': pending_custom_package_requests,
        'finished_custom_package_requests': finished_custom_package_requests
    }

    return render(request, 'dap_booking/dashboard.html', context)