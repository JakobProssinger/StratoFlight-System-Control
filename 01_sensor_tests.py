#!/usr/bin/python3
from src.sensors.ds18b20 import DS18B20
from src.sensors.ina260 import INA260
import src.sensors.internal
import time

TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f', '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]


def getTempSensorList(ds18b20_devices):
    temperature_list = [0.0] * len(ds18b20_devices)
    for i in range(0, len(ds18b20_devices), 1):
        temperature_list[i] = ds18b20_devices[i].getTemperature()
    return temperature_list


def get_Current_INA_List(ina260_devices):
    current_list = [0.0] * len(ina260_devices)
    for i in range(0, len(ina260_devices), 1):
        current_list[i] = ina260_devices[i].get_current()
    return current_list


def get_Bus_Voltage_INA_List(ina260_devices):
    voltage_list = [0.0] * len(ina260_devices)
    for i in range(0, len(ina260_devices), 1):
        voltage_list[i] = ina260_devices[i].get_bus_voltage()
    return voltage_list


def main():
    #setup
    #init ds18b20 Temperature Sensors
    ds18b20_sensors = []
    for device_address in TEMPSENSORS_DEVICE_ADDRESSES:
        ds18b20_sensors.append(DS18B20(device_address))

    #init ina260 Sensors
    ina260_sensors = []
    for device_address in INA260_DEVICE_ADDRESSES:
        temp_ina260 = INA260(device_address)
        temp_ina260.reset_chip()
        temp_ina260.activate_average(4)
        ina260_sensors.append(temp_ina260)

    min_Voltage = 10000.0  #mV
    voltage_List = [0.0, 0.0]
    while 1:

        #read ds18b20 Temperature Sensors
        print("Outer Temperature: ", getTempSensorList(ds18b20_sensors))

        #read raspberry internal Temperature
        print("Internal Temperature: ",
              src.sensors.internal.get_raspberry_temperature())

        #read ina260 current sensors
        print("Bus Current: ", get_Current_INA_List(ina260_sensors))
        #read ina260 bus voltage sensors
        voltage_List = get_Bus_Voltage_INA_List(ina260_sensors)

        print("Bus Voltage: ", voltage_List)
        if min_Voltage > voltage_List[1]:
            min_Voltage = voltage_List[1]
        print("Min Voltage: " + str(min_Voltage) + "\n")
        time.sleep(0.5)


if __name__ == '__main__':
    main()
