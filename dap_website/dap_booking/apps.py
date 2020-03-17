from django.apps import AppConfig


class DapBookingConfig(AppConfig):
    name = 'dap_booking'

    def ready(self):
        import dap_booking.signals