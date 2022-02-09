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

_SECONDARY1_REQUEST_SHUTDOWN_PIN = 32
_SECONDARY2_REQUEST_SHUTDOWN_PIN = 36
_SECONDARY3_REQUEST_SHUTDOWN_PIN = 38
_SECONDARY4_REQUEST_SHUTDOWN_PIN = 40
_REQUEST_SHUTDOWN_PINS = [_SECONDARY1_REQUEST_SHUTDOWN_PIN,
                          _SECONDARY2_REQUEST_SHUTDOWN_PIN,
                          _SECONDARY3_REQUEST_SHUTDOWN_PIN,
                          _SECONDARY4_REQUEST_SHUTDOWN_PIN]

_SECONDARY1_POWER_OFF_PIN = 29
_SECONDARY2_POWER_OFF_PIN = 31
_SECONDARY3_POWER_OFF_PIN = 33
_SECONDARY4_POWER_OFF_PIN = 35
_POWER_OFF_PINS = [_SECONDARY1_POWER_OFF_PIN,
                   _SECONDARY2_POWER_OFF_PIN,
                   _SECONDARY3_POWER_OFF_PIN,
                   _SECONDARY4_POWER_OFF_PIN]

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
_PRIMARY_INA260_ADDRESS = 0x40
_SECONDARY1_INA260_ADDRESS = 0x41  # jumper on A0
