"""
@File:          sensor_processor.py
@Descrption:    module for handling multible sensor measurings 
@Author:        Prossinger Jakob
@Date:          12 December 2021
@Todo:          * csv Error logging
                * remove minimal Values of Voltage
"""
from src.sensors.ina260 import INA260
from src.logging.csv_handler import CSVHandler
import src.sensors.internal as internal
import logging
import datetime

logger = logging.getLogger("strato_logger.sensor_process")


class SensorDataObject:
    def __init__(self, ina_current_list: list, ina_voltage_list: list,
                 raspberry_temperature: float) -> None:
        self.ina_current_data = ina_current_list
        self.ina_voltage_data = ina_voltage_list
        self.raspberry_temperature = raspberry_temperature


class SensorObject:
    def __init__(self, ina260_device_list: list,
                 csv_handler: CSVHandler) -> None:
        self.ina_devices = []
        ina_current = [0.0] * len(ina260_device_list)
        ina_voltage = [0.0] * len(ina260_device_list)
        self.sensor_data = SensorDataObject(ina_current,
                                            ina_voltage,
                                            raspberry_temperature=0.0)
        self.csv_handler = csv_handler
        self.min_INA_voltages = [1000000.0, 1000000.0]  #mV
        self.max_INA_voltages = [-1000000.0, -1000000.0]
        self.logger = logging.getLogger("strato_logger.sensor_process")

        for sensor in ina260_device_list:
            temp_sensor = INA260(sensor)
            temp_sensor.activate_average(4)
            self.ina_devices.append(temp_sensor)

        self.logger.info("created sensor_process object")

    def get_ina_current(self) -> float:
        return self.sensor_data.ina_current_data

    def get_ina_voltage(self) -> float:
        return self.sensor_data.ina_voltage_data

    def get_Current_INA_List(self) -> list:
        current_list = [0.0] * len(self.ina_devices)
        for i in range(0, len(self.ina_devices), 1):
            current_list[i] = self.ina_devices[i].get_current()
        return current_list

    def get_Bus_Voltage_INA_List(self) -> list:
        voltage_list = [0.0] * len(self.ina_devices)
        for i in range(0, len(self.ina_devices), 1):
            voltage_list[i] = self.ina_devices[i].get_bus_voltage()
        return voltage_list

    def reload_ina_data(self) -> None:
        self.sensor_data.ina_current_data = self.get_Current_INA_List()
        self.sensor_data.ina_voltage_data = self.get_Bus_Voltage_INA_List()

    def reload_raspberry_temperature(self) -> None:
        self.sensor_data.raspberry_temperature = internal.get_raspberry_temperature(
        )

    def reload_system_data(self) -> None:
        self.reload_ina_data()
        self.reload_raspberry_temperature()

    def system_process(self) -> None:
        self.csv_handler.csv_write_data_cell(datetime.datetime.now())
        self.reload_ina_data()

        #write INA current to CSV
        for values in self.sensor_data.ina_current_data:
            self.csv_handler.csv_write_data_cell(values)

        #write INA voltage to CSV
        for values in self.sensor_data.ina_voltage_data:
            self.csv_handler.csv_write_data_cell(values)

        #write onebaord raspberry pi temperature to csv
        self.reload_raspberry_temperature()
        self.csv_handler.csv_write_data_cell(
            self.sensor_data.raspberry_temperature)

        # print min an max voltage values

        for i in range(0, len(self.sensor_data.ina_voltage_data)):
            if type(self.sensor_data.ina_voltage_data[i]) == str:
                self.csv_handler.csv_write_data_cell(self.min_INA_voltages[i])
                self.csv_handler.csv_write_data_cell(self.max_INA_voltages[i])
                continue
            if self.min_INA_voltages[i] > self.sensor_data.ina_voltage_data[i]:
                self.min_INA_voltages[i] = self.sensor_data.ina_voltage_data[i]
            self.csv_handler.csv_write_data_cell(self.min_INA_voltages[i])
            if self.max_INA_voltages[i] < self.sensor_data.ina_voltage_data[i]:
                self.max_INA_voltages[i] = self.sensor_data.ina_voltage_data[i]
            self.csv_handler.csv_write_data_cell(self.max_INA_voltages[i])

        self.csv_handler.csv_write_newline()
