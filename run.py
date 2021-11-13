#!/usr/bin/python3
from os import name
from src.sensors.ds18b20 import DS18B20

DEVICE_ADRESS  = '28-00000cdfc36f'

def main():
    ds18b20A = DS18B20(DEVICE_ADRESS)
    print(ds18b20A.getTemperature())

if __name__ == '__main__':
    main()
