"""
@File:          constants.py
@Descrption:    Constants for the StratoFlight 2021/22 Project
                includes Sensor addresses, file-paths and const. strings
@Author:        Prossinger Jakob
@Date:          21 December 2021
@Todo:          * 
"""
#Server
_IP_PRIMARY = '10.11.0.1'

#PIN Layout
_LEDPIN1 = 11
_LEDPIN2 = 13
_ONEWIRE_PIN = 7  # GPIO 4

#Configure
_AUTOSTART_LED_BLINK = True
_AUTOSTART_MEASURING = True

#Sensors
_INA260_DEVICE_ADDRESSES = [0x40, 0x41]
_CSV_HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'raspberry temperature', 'min_Voltage1',
    'min_Voltage2', 'max_Voltage1', 'max_Voltage2'
]