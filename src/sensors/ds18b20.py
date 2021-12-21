"""
@File:          ds18b20.py
@Descrption:    a module to read temperature from a ds18b20
@Author:        Prossinger Jakob
@Date:          21 December 2021
@Todo:          * reset config register
"""
import logging

# setup for logging
ds18b20_module_logger = logging.getLogger(
    "strato_logger.sensor_process.ds18b20")


class DS18B20:
    """
    a class used to read from the ds18b20

    ...

    Attributes
    ----------
    ds18b20_module_logger : Logger
        a logger from the standard logger module. Child logger from strato_logger
    
    self.logger = ds18b20_module_logger

    self.device_address : str
        str with the address of a ds18b20 sensor

    _DS18B20_DEFAULT_DEVICE_ADDRESS : str
        default one-wire address of the sensor defined as 28-00000cdfc36f.
        Format is defined by the one-wire library from the raspberry pi.

    _DS18B20_DIRECTORY1 : str
        part one of the one-wire directory of the sensor. This path is 
        defined by the one-wire library from the raspberry pi.
    
    _DS18B20_DIRECTORY2 : str
        part one of the one-wire directory of the sensor. This path is 
        defined by the one-wire library from the raspberry pi.

    self.directory : str
        path of the one-wire file of the ds18b20.    
    
    Methods:
    ----------
    getTemperature : float
        reads the temperature from an ds18b20 via the 1-Wire bus

    """
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
        """
        read the temperature of a ds18b20

        Throws
        ------
        OSException
            if one-wire file could not be found
        
        return
        ------
            if reading was sucessful return temperature values in °C
            if file is corrupted return "File Error"
            else return str with "Sensor Missing".
        """
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