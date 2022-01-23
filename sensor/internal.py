"""
@File:          internal.py
@Descrption:    a module to hantel internal data from raspberry
@Author:        Prossinger Jakob
@Date:          23 January 2022
@Todo:          *
"""
import os
from sensor import sensor
from sensor.sensor_data import sensor_data
import datetime


class INTERNAL(sensor.Sensor):
    __DATA_NAMES = ["Raspberry Temperature", "Time"]
    __DATA_UNITS = ["°C", ""]

    def __init__(self, name: str) -> None:
        self.name = name
        self.device_address = "none"
        self.data = sensor_data(
            INTERNAL.__DATA_NAMES,
            [0.0, 0.0], INTERNAL.__DATA_UNITS, 2)

    def read_Sensor(self) -> None:
        self.data.data_value = [
            self.get_raspberry_temperature(), self.get_time()]

    def get_Data(self):
        return self.data

    def get_raspberry_temperature(self) -> float:
        try:
            cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
            return cpu_temp.replace("temp=", "")
        except Exception as e:
            logger.error("couldnt read CPU Temperature")
        return "noCPUTemperature"

    def get_time(self) -> str:
        return f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}'
