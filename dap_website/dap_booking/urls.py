from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'dap_booking'
urlpatterns = [
    path('', views.PackageListView.as_view(), name='home'),
    path('package/<str:pk>/', views.PackageDetailView.as_view(), name='package'),

    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('login', auth_views.LoginView.as_view(template_name='dap_booking/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='dap_booking/logout.html'), name='logout'),

    path('purchase/<str:pk>/', views.purchase, name='purchase'),
    path('passenger/details/<str:pk>/', views.passenger_details, name='passenger_details'),
    path('transaction/details/<str:pk>/', views.transaction_details, name='transaction_details'),

    path('custom_package_request/', views.custom_package_request, name='custom_package_request'),
    path('custom_package_request/details/<str:pk>/', views.custom_package_request_details, name='custom_package_request_details'),


    path('bookings/<str:pk>/', views.bookings, name='bookings'),
    path('custom_package_request_bookings/<str:pk>/', views.custom_package_request_bookings, name='custom_package_request_bookings'),
    path('dashboard/', views.dashboard, name='dashboard'),
]