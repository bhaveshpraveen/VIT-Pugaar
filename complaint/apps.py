from django.apps import AppConfig


class ComplaintConfig(AppConfig):
    name = 'complaint'

    def ready(self):
        import complaint.signals
