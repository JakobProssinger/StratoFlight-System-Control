"""
@File:          07_NEO-6M.py
@Descrption:    starts flask server for Strato Flight 2021/2022
@Author:        Prossinger Jakob
@Date:          19 January 2021
@Todo:          * 
"""
import serial
import os
import logging
import sensor
from sensor import sensor
from sensor.sensor_data import sensor_data

_NEO6M_DEFAULT_PORT = "/dev/ttyAMA0"
_NEO6M_DEFAULT_Directory = "/dev/ttyAMA0"


class NEO6M(sensor.Sensor):
    __DATA_NAMES = ["Longitude", "Latitude", "Altitude"]
    __DATA_UNITS = ["tbd", "tbd", "tbd"]

    def __init__(self, name: str, address: str = _NEO6M_DEFAULT_Directory, port: str = _NEO6M_DEFAULT_PORT):
        # self.sensor_type = _SENSOR_TYPE[_NEO6M]
        self.name = name
        self.directory = address
        self.port = port
        self.data = sensor_data.sensor_data(
            NEO6M.__DATA_NAMES,
            [0.0, 0.0, 0.0], NEO6M.__DATA_UNITS, 3)

    def read_Sensor(self):
        return "NEO6M_DATA"

    def get_Data(self):
        return self.data
