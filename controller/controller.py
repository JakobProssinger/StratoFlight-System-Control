"""
@File:          controller.py
@Descrption:    controlls sensor and secondary raspberries                
@Author:        Prossinger Jakob
@Date:          11 April 2022
@Todo:          
"""
from sensor.sensor import Sensor
from csv_handler.csv_handler import CSV_HANDLER
from controller.secondary.secondary import Secondary
from controller.secondary import secondary
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
        self.csv_handler: CSV_HANDLER = csv_handler
        self.secondaries = {}  # dictionary with all secndaries

    def get_Scondaries(self) -> dict:
        return self.secondaries

    def write_csv_header(self) -> None:
        """
        write the header file to the csv-file based on all sensors and secondaries
        """
        if path.getsize(self.csv_handler.path) != 0:
            #header is already in file
            return
        for sensor in self.sensors:
            for i in range(sensor.data.data_length):
                self.csv_handler.write_data_cell(
                    f'{sensor.name} {sensor.data.data_name[i]} [{sensor.data.data_unit[i]}]'
                )
        for secondary in self.get_Scondaries().values():
            self.csv_handler.write_data_cell(
                f'{secondary.get_Name()} Power Status')
        self.csv_handler.write_newline()

    def write_csv_data(self) -> None:
        """
        write all sensor data to the csv-file
        """
        for sensor in self.sensors:
            self.csv_handler.write_list(sensor.data.data_value)
        for secondary in self.get_Scondaries().values():
            if secondary.get_Power_status() == Secondary.SHUTDOWN:
                self.csv_handler.write_data_cell("off")
            else:
                self.csv_handler.write_data_cell("on")
        self.csv_handler.write_newline()

    def add_Secondary(self, secondary: Secondary) -> None:
        # add new Secondary to dictionary
        self.secondaries.update({secondary.get_Name(): secondary})

    def addSensor(self, sensor: Sensor) -> None:
        """
        add a sensor the controller instance

        Args:
            sensor (Sensor): sensor to add
        """
        self.sensors.append(sensor)

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

    def check_shutdown(self, ina_voltage: float) -> None:
        if type(ina_voltage) != float:
            return
        for raspberry in self.get_Scondaries().values():
            # continue to next raspberry if raspberry is already shutdowned
            if raspberry.get_Power_status() == secondary.Secondary.SHUTDOWN:
                if raspberry.get_Power_on_voltage() <= ina_voltage:
                    raspberry.turn_on()
                    print(f'turned on secondary : {raspberry.get_Name()}')
            elif raspberry.get_Shutdown_voltage() > ina_voltage:
                # request shutdown if shutdown has not been requested
                if raspberry.get_Request_status() == secondary.Secondary.NOT_SHUTDOWN_REQUEST:
                    raspberry.request_shutdown()
                    print(
                        f'request shutdown secondary : {raspberry.get_Name()}')
                # shutdown raspberry
                else:
                    raspberry.shutdown()
                    print(f'shutdown secondary : {raspberry.get_Name()}')
