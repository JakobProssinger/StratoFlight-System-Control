from src.sensors.ina260 import INA260
from src.sensors.ds18b20 import DS18B20
import src.sensors.internal as internal


class sensor_data_object:
    def __init__(self, ina260_device_list, ds18b20_device_list):
        self.ina_devices = []
        self.ds18b20_devices = []
        self.ina_current = [0.0] * len(ina260_device_list)
        self.ina_voltage = [0.0] * len(ina260_device_list)
        self.raspberry_temperature = 0.0
        for sensor in ina260_device_list:
            temp_sensor = INA260(sensor)
            # temp_sensor.reset_chip()
            temp_sensor.activate_average(4)
            self.ina_devices.append(temp_sensor)

        for sensor in ds18b20_device_list:
            temp_sensor = DS18B20(sensor)
            self.ds18b20_devices.append(temp_sensor)
        self.ds18b20_values = [0.0] * len(ds18b20_device_list)

    def get_ina_current(self):
        return self.ina_current

    def get_ina_voltage(self):
        return self.ina_voltage

    def reload_ina_data(self):
        self.ina_current = self.get_Current_INA_List()
        self.ina_voltage = self.get_Bus_Voltage_INA_List()

    def reload_ds_temperature(self):
        temperature_list = [0.0] * len(self.ds18b20_devices)
        for i in range(0, len(self.ds18b20_devices), 1):
            temperature_list[i] = self.ds18b20_devices[i].getTemperature()
        self.ds18b20_values = temperature_list

    def reload_raspberry_temperature(self):
        self.raspberry_temperature = internal.get_raspberry_temperature()

    def get_Current_INA_List(self):
        current_list = [0.0] * len(self.ina_devices)
        for i in range(0, len(self.ina_devices), 1):
            current_list[i] = self.ina_devices[i].get_current()
        return current_list

    def get_Bus_Voltage_INA_List(self):
        voltage_list = [0.0] * len(self.ina_devices)
        for i in range(0, len(self.ina_devices), 1):
            voltage_list[i] = self.ina_devices[i].get_bus_voltage()
        return voltage_list

    def reload_system_data(self):
        self.reload_ina_data()
        self.reload_ds_temperature()
        self.reload_raspberry_temperature()
