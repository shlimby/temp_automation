from django.apps import AppConfig
import sys
import os


class TempAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'temp_app'

    # Shedulers with schedule
    def ready(self) -> None:
        ret = super().ready()

        # Runs code only once and when app is running as server: https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds/44897678
        if os.environ.get('RUN_MAIN', None) != 'true' and ('runserver' in sys.argv or not 'manage.py' in sys.argv):
            # Import here, as the models has to be loaded
            from . import jobs

            jobs.get_weather_data()
            jobs.start_scheduler()

        return ret
