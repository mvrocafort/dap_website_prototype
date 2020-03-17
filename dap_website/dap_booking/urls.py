from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'dap_booking'
urlpatterns = [
    path('', views.PackageListView.as_view(), name='home'),

    path('login', auth_views.LoginView.as_view(template_name='dap_booking/login.html'), name='login'),
    path('register', views.register, name='register'),

    path('package/<str:pk>/', views.PackageDetailView.as_view(), name='package'),

    path('purchase/<str:pk>/', views.purchase, name='purchase'),
    path('passenger/details/<str:pk>/', views.passenger_details, name='passenger_details'),
    path('transaction/details/<str:pk>/', views.transaction_details, name='transaction_details'),
]