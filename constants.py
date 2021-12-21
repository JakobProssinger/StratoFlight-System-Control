"""
@File:          constants.py
@Descrption:    Constants for the StratoFlight 2021/22 Project
                includes Sensor addresses, file-paths and konst. strings
@Author:        Prossinger Jakob
@Date:          21 December 2021
@Todo:          * 
"""
_LEDPIN1 = 11
_LEDPIN2 = 13
_ONEWIRE_PIN = 7  # GPIO 4
_DS18b20_ADDRESSES = ['28-00000cdfc36f']
_INA260_DEVICE_ADDRESSES = [0x40, 0x41]
_CSV_HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'ds18b28 Temperature', 'raspberry temperature'
]