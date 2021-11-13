import sys, os

class DS18B20:

    _DS18B20_DEFAULT_DEVICE_ADDRESS = "28-00000cdfc36f"
    _DS18B20_FOLDER_STRUCTURE1 = '/sys/bus/w1/devices/'
    _DS18B20_FOLDER_STRUCTURE2 = '/w1_slave'

        #Constructor
    def __init__(self, device_address=_DS18B20_DEFAULT_DEVICE_ADDRESS):
        self.device_adress = device_address
        self.folder_structure = self._DS18B20_FOLDER_STRUCTURE1 + self.device_adress + self._DS18B20_FOLDER_STRUCTURE2

    def getTemperature(self):
        try:
            file = open(self.folder_structure)
        except OSError:
            return 'Sensor Missing'
        else:
            filecontent = file.read()
            file.close()

			# Error in Temperatursensor Daten
            if len(filecontent) != 75:
                return 'File Error'
            else:
                stringvalue = filecontent.split("\n")[1].split(" ")[9]
                return float(stringvalue[2:]) / 1000
