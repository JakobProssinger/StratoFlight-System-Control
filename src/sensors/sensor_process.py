from src.sensors.ina260 import INA260
from src.sensors.ds18b20 import DS18B20
import src.sensors.internal as internal
import logging

module_logger = logging.getLogger("strato_logger.sensor_process")


class sensor_data_object:
    def __init__(self, ina_current_list: list, ina_voltage_list: list,
                 ds18b20_temperature_list: list,
                 raspberry_temperature: float) -> None:
        self.ina_current_data = ina_current_list
        self.ina_voltage_data = ina_voltage_list
        self.ds18_temperature_data = ds18b20_temperature_list
        self.raspberry_temperature = raspberry_temperature


class sensor_object:
    def __init__(self, ina260_device_list: list,
                 ds18b20_device_list: list) -> None:
        self.ina_devices = []
        self.ds18b20_devices = []
        ina_current = [0.0] * len(ina260_device_list)
        ina_voltage = [0.0] * len(ina260_device_list)
        ds18b20_temperature = [0.0] * len(ds18b20_device_list)
        self.sensor_data = sensor_data_object(ina_current,
                                              ina_voltage,
                                              ds18b20_temperature,
                                              raspberry_temperature=0.0)

        for sensor in ina260_device_list:
            temp_sensor = INA260(sensor)
            temp_sensor.activate_average(4)
            self.ina_devices.append(temp_sensor)

        for sensor in ds18b20_device_list:
            temp_sensor = DS18B20(sensor)
            self.ds18b20_devices.append(temp_sensor)

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

    def reload_ds_temperature(self) -> None:
        temperature_list = [0.0] * len(self.ds18b20_devices)
        for i in range(0, len(self.ds18b20_devices), 1):
            temperature_list[i] = self.ds18b20_devices[i].getTemperature()
        self.sensor_data.ds18_temperature_data = temperature_list

    def reload_raspberry_temperature(self) -> None:
        self.sensor_data.raspberry_temperature = internal.get_raspberry_temperature(
        )

    def reload_system_data(self) -> None:
        self.reload_ina_data()
        self.reload_ds_temperature()
        self.reload_raspberry_temperature()