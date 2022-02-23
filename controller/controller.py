"""
@File:          controller.py
@Descrption:    controlls sensor and secondary raspberries                
@Author:        Prossinger Jakob
@Date:          23 February 2022
@Todo:          * change sensor and sensor name to dictionary
"""
from sensor.sensor import Sensor
from csv_handler.csv_handler import CSV_HANDLER
from controller.secondary.secondary import Secondary
from os import path


class Controller():
    """
    a controller to handle multiple sensors of the Sensor class
    """

    def __init__(self, name: str, csv_handler: CSV_HANDLER) -> None:
        """
        init function for Controller class 

        Args:
            name (str): name of the controller
            csv_handler (CSV_HANDLER): csv_handler to store the data of all sensors
        """
        self.name: str = name
        self.sensors: list = []
        self.sensor_names: list = []
        self.csv_handler: CSV_HANDLER = csv_handler
        self.secondaries = {}  # dictionary with all secndaries

    def get_Scondaries(self) -> dict:
        return self.secondaries

    def write_csv_header(self) -> None:
        """
        write the header file to the csv-file based on all sensors
        """
        if path.getsize(self.csv_handler.path) != 0:
            return
        for sensor in self.sensors:
            for i in range(sensor.data.data_length):
                self.csv_handler.csv_write_data_cell(
                    f'{sensor.name} {sensor.data.data_name[i]} [{sensor.data.data_unit[i]}]'
                )
        self.csv_handler.csv_write_newline()

    def write_csv_data(self) -> None:
        """
        write all sensor data to the csv-file
        """
        for sensor in self.sensors:
            self.csv_handler.csv_write_list(sensor.data.data_value)
        self.csv_handler.csv_write_newline()

    def add_Secondary(self, secondary: Secondary) -> None:
        # add new Secondary to dictionary
        self.secondaries.update({secondary.get_Name(): secondary})

    def secondary_request_shutdown(self, name: str) -> None:
        self.secondaries[name].request_shutdown()

    def secondary_shutdown(self, name: str) -> None:
        self.secondaries[name].shutdown()

    def addSensor(self, sensor: Sensor) -> None:
        """
        add a sensor the controller instance

        Args:
            sensor (Sensor): sensor to add
        """
        self.sensors.append(sensor)
        self.sensor_names.append(sensor.name)

    def print_data(self) -> None:
        """
        print the data of all sensors to the cli
        """
        for sensor in self.sensors:
            print(sensor.get_Data())

    def reload(self) -> None:
        """
        read all sensors data and store in the the sensor.data object
        """
        for sensor in self.sensors:
            sensor.read_Sensor()
