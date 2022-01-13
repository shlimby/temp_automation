
# Works for linux only
# from .models import Place
from os import cpu_count
from schedule import Scheduler
from datetime import datetime, timedelta, timezone
import requests
import threading
import time

from temp_app.common import get_settings

from .models import OutsideEntrie, Place

init_sched = False
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

MAX_CALLS_PER_MONTH = 1_000_000  # Calls/month
MAX_CALLS_PER_MINUTE = 60  # calls/minute
MAX_CALLS_PER_SECOND = MAX_CALLS_PER_MINUTE / 60  # calls/second
MAX_DAYS_PER_MONTH = 31
MAX_CALLS_PER_MINUTE_LONGTERME = MAX_CALLS_PER_MONTH / \
    (MAX_DAYS_PER_MONTH * 24 * 60)  # 22.41
# Minute/Jobs -> every 5 minutes start job for each api
MIN_WAITING_TIME_WEATHER_API = 5  # 22.14*5 = 110 calls => 110 Places is max

# waiting_per_call = 0

# cnt_places = Place.objects.count()


def get_sleep_time():
    resulting_calls = Place.objects.count()  # minute

    # Too many calls as for each place on call will be made
    if resulting_calls >= MAX_CALLS_PER_MINUTE:
        return 1  # secodnds => 60 Calls/minute
    else:
        return 0


def get_zipcode_url(zip_code: str, country_code: str, api_key: str):
    """Returns '?zip={zip_code},{country_code}&appid={api_key}'
    """
    return '?zip={zip_code},{country_code}&units=metric&appid={api_key}'.format(zip_code=zip_code, country_code=country_code, api_key=api_key)


def get_lat_url(lat: str, long: str, api_key: str):
    """ Returns '?lat={lat}&lon={long}&appid={api_key}'
    """
    return '?lat={lat}&lon={long}&units=metric&appid={api_key}'.format(lat=lat, long=long, api_key=api_key)


def get_weather_data():
    """ Makes API Call for ervey place in the Table
    and saves data in OutsideEntries
    """

    API_KEY = get_settings().get('api_key').get('value')

    places = Place.objects.all()
    sleep = get_sleep_time()

    for place in places:

        url = WEATHER_BASE_URL
        print("Get weather-data from: " + str(place))

        # Get url by data
        if place.longitude != None and place.latitude != None:
            url += get_lat_url(str(place.latitude),
                               str(place.longitude), API_KEY)
        else:
            url += get_zipcode_url(place.zip_code, place.country_code, API_KEY)

        # Make request
        responce = requests.get(url)

        if responce.status_code == 200:
            json = responce.json()
            try:
                main = json.get('main')

                tz = timezone(timedelta(seconds=json.get('timezone')))
                dt = datetime.fromtimestamp(
                    json.get('dt'),
                    tz)

                entry = OutsideEntrie(
                    timestamp=dt,
                    temp=main.get('temp'),
                    humidity=main.get('humidity'),
                    pressure=main.get('pressure'),
                    place=place,
                )
                entry.save()
            except Exception as e:
                print("Not able to parse responce of OpenWeather:")
                print(e.args)
        # sleep in order to stay inside of MAX_CALLS_PER_SECOND
        time.sleep(sleep)


# https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds/44897678
def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    https://schedule.readthedocs.io/en/stable/background-execution.html
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run  # ^= stop_run_continouisly


# Change run_continuously method
Scheduler.run_continuously = run_continuously


def start_scheduler():
    """Starts Scheduler"""
    print('Start Scheduler')
    scheduler = Scheduler()
    scheduler.every(MIN_WAITING_TIME_WEATHER_API).minutes.do(get_weather_data)
    scheduler.run_continuously()
