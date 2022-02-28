"""
@File:          AM2302.py
@Descrption:    module to read AM2302 or DHT22
@Author:        Prossinger Jakob
@Date:          23 February 2022
@Todo:          * add logging
"""
from sensor import sensor
from sensor.sensor_data import sensor_data
import Adafruit_DHT


class AM2302(sensor.Sensor):
    __DATA_NAMES = ["Temperature", "Humidity"]
    __DATA_UNITS = ["°C", "mV"]

    def __init__(self, name: str):
        self.name = name
        self.sensor_type = sensor._SENSOR_TYPE[sensor._AM2302]
        self.data = sensor_data.sensor_data(
            AM2302.__DATA_NAMES,
            [0.0, 0.0], AM2302.__DATA_UNITS, 2)

    def read_Sensor(self) -> list:
        # TODO convert to °C
        try:
            humidity, temperature = Adafruit_DHT.read_retry(
                Adafruit_DHT.DHT22, 4)
        except:
            humidity = "notFound"
            temperature = "notFound"
        finally:
            self.data.data_value = [temperature, humidity]

    def get_Data(self) -> sensor_data.sensor_data:
        return self.data
