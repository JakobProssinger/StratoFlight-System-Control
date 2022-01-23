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
    data_name: list
    data_value: list
    data_unit: list
    data_length: int
