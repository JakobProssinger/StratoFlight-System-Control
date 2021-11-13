#!/usr/bin/python3
from os import name
from src.sensors.ds18b20 import DS18B20

TEMPSENSORS_DEVICE_ADRESSES = ['28-00000cdfc36f', '28-00000cdf6b81']

def getTempSensorList(ds18b20_devices):
    temperature_list = [0.0] * len(ds18b20_devices)
    flag = 0
    for device in ds18b20_devices, :
        temperature_list[flag] = ds18b20_devices[flag].getTemperature()
        flag += 1
    return temperature_list

def main():
    #init ds18b20 Temperature Sensors
    ds18b20_sensors = []
    for device_address in TEMPSENSORS_DEVICE_ADRESSES:
        ds18b20_sensors.append(DS18B20(device_address))
    #read ds18b20 Temperature Sensors
    print(getTempSensorList(ds18b20_sensors))

if __name__ == '__main__':
    main()
