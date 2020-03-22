from django.apps import AppConfig


class DapBookingConfig(AppConfig):
    name = 'dap_booking'
    verbose_name = 'Discover Asia Philippines'

    def ready(self):
        import dap_booking.signals