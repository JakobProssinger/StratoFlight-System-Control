"""
@File:          sensor.py
@Descrption:    module to handle multiple sensors reading
@Author:        Prossinger Jakob
@Date:          5 March 2022
@Todo:          
"""


class Sensor():
    """
    sensor class, parent class for sensors

    """
    name: str

    def read_Sensor(self) -> list:
        pass

    def get_Data(self) -> None:
        pass
