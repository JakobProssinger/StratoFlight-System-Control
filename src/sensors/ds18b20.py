import sys
import os
import logging

# setup for logging
ina_module_logger = logging.getLogger("strato_logger.sensor_process.ds18b20")


class DS18B20:

    _DS18B20_DEFAULT_DEVICE_ADDRESS = "28-00000cdfc36f"
    _DS18B20_DIRECTORY1 = '/sys/bus/w1/devices/'
    _DS18B20_DIRECTORY2 = '/w1_slave'

    #Constructor
    def __init__(
            self,
            device_address: str = _DS18B20_DEFAULT_DEVICE_ADDRESS) -> None:
        self.device_adress = device_address
        self.directory = self._DS18B20_DIRECTORY1 + self.device_adress + self._DS18B20_DIRECTORY2
        self.logger = logging.getLogger(
            "strato_logger.sensor_process.ds18b20.DS18B20")
        self.logger.info("created ds18b20 object")

    def getTemperature(self) -> float:
        try:
            with open(self.directory, 'r') as file:
                filecontent = file.read()
        except OSError:
            self.logger.error("couldn't read ds18b20 sensor")
            return 'Sensor Missing'

        # Error in Temperatursensor Daten
        if len(filecontent) != 75:
            self.logger.error("file error ds18b20 sensor")
            return 'File Error'
        stringvalue = filecontent.split("\n")[1].split(" ")[9]
        return float(stringvalue[2:]) / 1000