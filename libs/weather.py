import threading
import time
import python_weather
import asyncio
import xml
import logging
from PIL import Image


try:
    from local_settings import WEATHER_FORMAT
except ImportError:
    WEATHER_FORMAT = python_weather.IMPERIAL

try:
    from local_settings import WEATHER_CITY
except ImportError:
    WEATHER_CITY = "Richmond, VA"

try:
    from local_settings import WEATHER_REFRESH
except ImportError:
    WEATHER_REFRESH = 900


logger = logging.getLogger("pitftmanager.libs.weather")


class Weather(threading.Thread):
    """
    This class provides access to the weather info
    """
    weather = None
    refresh_interval: int = WEATHER_REFRESH
    loop = asyncio.get_event_loop()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    thread_lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.name = "Weather"
        self.shutdown = threading.Event()

    def run(self) -> None:
        thread_process = threading.Thread(target=self.weather_loop)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()
        self.shutdown.wait()

    def weather_loop(self):
        while not self.shutdown.is_set():
            self.refresh_interval -= 1
            time.sleep(1)
            if self.refresh_interval < 1:
                try:
                    self.loop.run_until_complete(self.update())
                except xml.parsers.expat.ExpatError as error:
                    logger.warning(error)
                self.refresh_interval = WEATHER_REFRESH

    def stop(self):
        self.shutdown.set()

    async def update(self):
        """
        Update the weather info
        :return: None
        add locale=python_weather.Locale.ITALIAN if needed
        """
        logger.debug('weather update CALLED!')
        self.thread_lock.acquire()
        client = python_weather.Client(unit=WEATHER_FORMAT)
        self.weather = await client.get(WEATHER_CITY)
        await client.close()
        self.thread_lock.release()

    def get_temperature(self):
        """
        Get the temperature
        :return: String of the temperature
        """
        if not self.weather:
            return "--"

        return self.weather.current.temperature

    def get_sky_text(self):
        """
        Get the sky text
        :return: String of the sky text
        """
        if not self.weather:
            return "--"

        return self.weather.current.description

    def get_location_name(self):
        """
        Get the location name
        :return: String of the location name
        """
        if not self.weather:
            return "--"

        return self.weather.nearest_area.name

    def get_icon(self):
        """
        Get the icon for the current weather
        :return: emoji str
        """
        if not self.weather:
            return "-"

        return self.weather.current.kind.emoji
    
    def get_moon(self):
        """
        Get the moon phase for the current weather
        :return: emoji str
        """
        if not self.weather:
            return "-"

        for forecast in self.weather.forecasts:
            moon = forecast.astronomy.moon_phase.emoji
            break
        return moon


weather: Weather = Weather()


def get_weather():
    """
    Get the main weather object
    :return: Weather
    """
    # update_weather()
    return weather


def update_weather():
    """
    Update the weather info
    :return: None
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(weather.update())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    update_weather()
    logger.info(weather.weather.current.description)
