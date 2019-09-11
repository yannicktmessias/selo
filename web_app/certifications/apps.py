from django.apps import AppConfig


class CertificationsConfig(AppConfig):
    name = 'certifications'

    def ready(self):
        from reports_updater import updater
        updater.start()