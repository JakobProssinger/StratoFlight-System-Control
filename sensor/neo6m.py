"""
@File:          neo6m.py
@Descrption:    module to read Neo-6M GPS Sensor
@Author:        Prossinger Jakob
@Date:          23 January 2021
@Todo:          * implement real sensor readin
"""
import serial
import os
import logging
import sensor
from sensor import sensor
from sensor.sensor_data import sensor_data

_NEO6M_DEFAULT_Directory = "/dev/ttyAMA0"


class NEO6M(sensor.Sensor):
    __DATA_NAMES = ["Longitude", "Latitude", "Altitude"]
    __DATA_UNITS = ["tbd", "tbd", "tbd"]

    def __init__(self, name: str, directory: str = _NEO6M_DEFAULT_Directory):
        # self.sensor_type = _SENSOR_TYPE[_NEO6M]
        self.name = name
        self.directory = directory
        self.data = sensor_data.sensor_data(
            NEO6M.__DATA_NAMES,
            [0.0, 0.0, 0.0], NEO6M.__DATA_UNITS, 3)

    def read_Sensor(self):
        return "NEO6M_DATA"

    def get_Data(self):
        return self.data
