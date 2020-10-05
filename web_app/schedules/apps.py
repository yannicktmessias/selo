from django.apps import AppConfig


class SchedulesConfig(AppConfig):
    name = 'schedules'

    def ready(self):
        from . import reports_updater, mail
        reports_updater.start()
        mail.start()