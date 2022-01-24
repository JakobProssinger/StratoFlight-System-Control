"""
@File:          internal.py
@Descrption:    a module to hantel internal data from raspberry
@Author:        Prossinger Jakob
@Date:          24 January 2022
@Todo:          *
"""
import os
from sensor import sensor
from sensor.sensor_data import sensor_data
import datetime


class INTERNAL(sensor.Sensor):
    __DATA_NAMES = ["Time", "Raspberry Temperature"]
    __DATA_UNITS = ["", "°C"]

    def __init__(self, name: str) -> None:
        self.name = name
        self.device_address = "none"
        self.data = sensor_data.sensor_data(
            INTERNAL.__DATA_NAMES,
            [0.0, 0.0], INTERNAL.__DATA_UNITS, 2)

    def read_Sensor(self) -> None:
        self.data.data_value = [self.get_time(),
                                self.get_raspberry_temperature()]

    def get_Data(self) -> sensor_data.sensor_data:
        return self.data

    def get_raspberry_temperature(self) -> float:
        try:
            cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
            return cpu_temp.replace("temp=", "")
        except Exception as e:
            logger.error("couldnt read CPU Temperature")
        return "noCPUTemperature"

    def get_time(self) -> str:
        return datetime.datetime.now()
