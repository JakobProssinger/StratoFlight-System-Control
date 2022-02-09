"""
@File:          controller.py
@Descrption:    controlls sensor and secondary raspberries                
@Author:        Prossinger Jakob
@Date:          9 February 2022
@Todo:          * add Raspberry secondary 
"""
from sensor.sensor import Sensor
from csv_handler.csv_handler import CSV_HANDLER
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
