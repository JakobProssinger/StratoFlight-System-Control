import sys
import os


class DS18B20:

    _DS18B20_DEFAULT_DEVICE_ADDRESS = "28-00000cdfc36f"
    _DS18B20_DIRECTORY1 = '/sys/bus/w1/devices/'
    _DS18B20_DIRECTORY2 = '/w1_slave'

    #Constructor
    def __init__(self, device_address: str = _DS18B20_DEFAULT_DEVICE_ADDRESS) -> None:
        self.device_adress = device_address
        self.directory = self._DS18B20_DIRECTORY1 + self.device_adress + self._DS18B20_DIRECTORY2

    def getTemperature(self) -> float:
        try:
            with open(self.directory, 'r') as file:
                filecontent = file.read()
        except OSError:
            return 'Sensor Missing'

        # Error in Temperatursensor Daten
        if len(filecontent) != 75:
            return 'File Error'
        else:
            stringvalue = filecontent.split("\n")[1].split(" ")[9]
            return float(stringvalue[2:]) / 1000