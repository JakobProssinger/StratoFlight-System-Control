"""
@File:          sensor_data.py
@Descrption:    class to store sensor data
@Author:        Prossinger Jakob
@Date:          23 January 2022
@Todo:          *
"""
from dataclasses import dataclass


@dataclass
class sensor_data:
    """
    class to store data of sensors

    Parameter:
        data_name (list): list with all names of the data from the sensor measures
        data_value (list): list with all measured values from the sensor 
        data_unit(list): list with all units of the measured values from the sensor
        data_length(list): lenght of the list above
    """
    data_name: list
    data_value: list
    data_unit: list
    data_length: int
