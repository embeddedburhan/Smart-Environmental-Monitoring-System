
import random
from datetime import datetime


class EnvironmentalSensorSimulator:
    """
    Simulates environmental sensor readings.

    Sensors:
    - Temperature
    - Relative humidity
    - Air quality

    Note: These values are simulated, not hardware measurements.
    """

    def __init__(self):
        self.temperature = 25.0
        self.humidity = 60.0
        self.air_quality = 45.0

    def read_temperature(self):
        self.temperature += random.uniform(-1.0, 1.0)
        self.temperature = max(15.0, min(40.0, self.temperature))
        return round(self.temperature, 2)

    def read_humidity(self):
        self.humidity += random.uniform(-2.0, 2.0)
        self.humidity = max(20.0, min(95.0, self.humidity))
        return round(self.humidity, 2)

    def read_air_quality(self):
        self.air_quality += random.uniform(-5.0, 5.0)
        self.air_quality = max(10.0, min(200.0, self.air_quality))
        return round(self.air_quality, 2)

    def read_all(self):
        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "temperature": self.read_temperature(),
            "humidity": self.read_humidity(),
            "air_quality": self.read_air_quality()
        }
