from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.conf import settings
from .models import Package
from .forms import UserRegisterForm


# Create your views here.
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


class PackageListView(ListView):
    model = Package
    template_name = 'dap_booking/home.html'
    context_object_name = 'packages'
    ordering = ['-date_created']  # display the latest package created on top


class PackageDetailView(DetailView):
    model = Package
    template_name = 'dap_booking/package.html'
