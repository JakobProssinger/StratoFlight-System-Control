"""
@File:          sensor.py
@Descrption:    module to handle multiple sensors reading
@Author:        Prossinger Jakob
@Date:          23 February 2022
@Todo:          
"""

_INA260 = 0
_DS18B20 = 1
_NEO6M = 2
_SENSOR_TYPE = {_INA260: "INA260",  _DS18B20: "DS18B20",
                _NEO6M: "NEO6M", _AM2302: "AM2302"}


class Sensor():
    """
    sensor class, parent class for sensors

    """
    name: str

    def read_Sensor(self) -> list:
        pass

    def get_Data(self) -> None:
        pass
