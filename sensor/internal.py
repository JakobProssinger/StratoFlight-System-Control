"""
@File:          internal.py
@Descrption:    a module to hantel internal data from raspberry
@Author:        Prossinger Jakob
@Date:          15 March 2022
@Todo:          *
"""
import os
from sensor import sensor
from sensor.sensor_data import sensor_data
import datetime
import config
import RPi.GPIO as GPIO


class INTERNAL(sensor.Sensor):
    """
    class to read internal data from the raspberry pi

    Attributes:
        __DATA_NAMES (list): stores the names for the data points of the internal sensor

        __DATA_UNITS (list): stores the units for the data point of the internal sensor
    """
    __DATA_NAMES = ["Date/Time", "Raspberry Temperature", "Start Ramp"]
    __DATA_UNITS = ["", "°C", ""]

    def __init__(self, name: str) -> None:
        """
        init function of the INTERNAL class

        Args:
            name (str): name of the internal sensor
        """
        self.name = name
        self.device_address = "none"
        self.data = sensor_data.sensor_data(
            INTERNAL.__DATA_NAMES,
            [0.0, 0.0], INTERNAL.__DATA_UNITS, 3)

    def read_Sensor(self) -> None:
        """
        read data from the raspberry pi and store it in the self.data object
        """
        self.data.data_value = [self.get_time(),
                                self.get_raspberry_temperature(),
                                self.get_start_ramp()]

    def get_Data(self) -> sensor_data.sensor_data:
        """
        read data from the self.data object

        Returns:
            sensor_data.sensor_data: data of the INTERNAL sensor
        """
        return self.data

    def get_raspberry_temperature(self) -> float:
        """
        read the temperature of the raspberry

        Returns:
            float: temperature of the raspberry if not possible return
                    string with noCPUTemperature
        """
        try:
            cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
            return cpu_temp.replace("temp=", "")
        except Exception as e:
            print("couldn't read CPU Temperature")
        return "noCPUTemperature"

    def get_time(self) -> str:
        """
        return time from the raspberry pi

        Returns:
            str: datetime of the raspberry
        """
        return datetime.datetime.now()

    def get_start_ramp(self) -> str:
        if GPIO.input(config._START_RAMP_PIN) is GPIO.HIGH:
            return "connected"
        return "not-connected"
