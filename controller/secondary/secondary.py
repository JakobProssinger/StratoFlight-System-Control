"""
@File:          secondary.py
@Descrption:    
@Author:        Prossinger Jakob
@Date:          22 February 2022
@Todo:          * 
"""
import RPi.GPIO as GPIO


class Secondary():
    _SHUTDOWN_REQUEST = GPIO.HIGH
    _NOT_SHUTDOWN_REQUEST = GPIO.LOW

    _SHUTDOWN = GPIO.LOW
    _NOT_SHUTDOWN = GPIO.HIGH

    def __init__(self, raspberry_name: str, request_pin: int,
                 power_off_pin: int):
        self.name: str = raspberry_name
        self.request_pin: int = request_pin
        self.power_off_pin: int = power_off_pin
        self._request_status: bool = Secondary._NOT_SHUTDOWN_REQUEST
        self._power_off_status: bool = Secondary._NOT_SHUTDOWN

    def get_Name(self) -> str:
        return self.name

    def request_shutdown(self) -> None:
        GPIO.output(self.request_pin, Secondary._SHUTDOWN_REQUEST)
        self._request_status = Secondary._SHUTDOWN_REQUEST

    def shutdown(self) -> None:
        GPIO.output(self.power_off_pin, Secondary._SHUTDOWN)
        self._power_off_status = Secondary._SHUTDOWN

    def boot(self) -> None:
        GPIO.output(self.power_off_pin, Secondary._NOT_SHUTDOWN)
        self._power_off_status = Secondary._NOT_SHUTDOWN
        GPIO.output(self.request_pin, Secondary._NOT_SHUTDOWN_REQUEST)
        self._request_status = Secondary._NOT_SHUTDOWN_REQUEST
