from csv_handler.csv_handler import CSV_HANDLER

_INA260 = 0
_DS18B20 = 1
_NEO6M = 2
_SENSOR_TYPE = {_INA260: "INA260",  _DS18B20: "DS18B20", _NEO6M: "NEO6M"}


class Sensor(object):
    name: str

    def write_to_csv() -> None:
        return None


class Controller(object):
    def __init__(self, name: str, csv_handler: CSV_HANDLER):
        self.name = name
        self.sensors: list = []
        self.sensor_names: list = []
        self.csv_handler: CSV_HANDLER = csv_handler

    def addSensor(self, sensor) -> None:
        self.sensors.append(sensor)
        self.sensor_names.append(sensor.name)

    def print_data(self) -> None:
        for sensor in self.sensors:
            print(sensor.get_Data())

    def reload(self) -> None:
        for sensor in self.sensors:
            pass
