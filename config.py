"""
@File:          config.py
@Descrption:    configure file for Strato FLight 2021/2022
@Author:        Prossinger Jakob
@Date:          23 January 2022
@Todo:          *
"""
import RPi.GPIO as GPIO
# Server
_IP_PRIMARY = '10.11.0.1'


# PIN Layout
_LED_PIN_RED = 11
_LED_PIN_GREEN = 13
_ONEWIRE_PIN = 7  # GPIO 4


# Configure
_AUTOSTART_LED_BLINK = True
_AUTOSTART_MEASURING = True

# LED
default_LED_states = {

    _LED_PIN_RED: {
        'name': "Red_LED_PIN",
        'state': GPIO.HIGH
    },
    _LED_PIN_GREEN: {
        'name': "Green_LED_PIN",
        'state': GPIO.LOW
    }
}

# Sensors
_INA260_DEVICE_ADDRESSES = [0x40, 0x41]
_CSV_HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'raspberry temperature', 'min_Voltage1',
    'min_Voltage2', 'max_Voltage1', 'max_Voltage2'
]
