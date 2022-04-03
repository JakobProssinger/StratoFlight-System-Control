"""
@File:          sensor.py
@Descrption:    module to handle multiple sensors reading
@Author:        Prossinger Jakob
@Date:          5 March 2022
@Todo:          
"""
from sensor.sensor_data import sensor_data


class Sensor():
    """
    sensor class, parent class for sensors

    """
    name: str
    data: sensor_data.sensor_data

    def read_Sensor(self) -> list:
        pass

    def get_Data(self) -> None:
        pass
