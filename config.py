"""
@File:          config.py
@Descrption:    configure file for Strato FLight 2021/2022
@Author:        Prossinger Jakob
@Date:          24 January 2022
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
_BLINK_INTERVAL_SEC = 1.5
_MEASURING_INTERVAL_SEC = 20

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
