"""
@File:          secondary.py
@Descrption:    
@Author:        Prossinger Jakob
@Date:          23 February 2022
@Todo:          * 
"""
import RPi.GPIO as GPIO


class Secondary():
    # TODO change to global
    SHUTDOWN_REQUEST = GPIO.HIGH
    NOT_SHUTDOWN_REQUEST = GPIO.LOW

    SHUTDOWN = GPIO.LOW
    NOT_SHUTDOWN = GPIO.HIGH

    def __init__(self, raspberry_name: str, request_pin: int,
                 power_off_pin: int, shutdown_voltage: float, power_on_voltage: float):
        self.name: str = raspberry_name
        self.request_pin: int = request_pin
        self.power_off_pin: int = power_off_pin
        self._request_status: bool = Secondary.NOT_SHUTDOWN_REQUEST
        self._power_off_status: bool = Secondary.NOT_SHUTDOWN
        self.shutdown_voltage: float = shutdown_voltage
        self.power_on_voltage: float = power_on_voltage

    def get_Name(self) -> str:
        return self.name

    def get_Power_off_status(self) -> bool:
        return self._power_off_status

    def get_Request_status(self) -> bool:
        return self._request_status

    def get_Shutdown_voltage(self) -> float:
        return self.shutdown_voltage

    def get_Power_on_voltage(self) -> float:
        return self.power_on_voltage

    def request_shutdown(self) -> None:
        GPIO.output(self.request_pin, Secondary.SHUTDOWN_REQUEST)
        self._request_status = Secondary.SHUTDOWN_REQUEST

    def shutdown(self) -> None:
        GPIO.output(self.power_off_pin, Secondary.SHUTDOWN)
        self._power_off_status = Secondary.SHUTDOWN

    def turn_on(self) -> None:
        GPIO.output(self.power_off_pin, Secondary.NOT_SHUTDOWN)
        self._power_off_status = Secondary.NOT_SHUTDOWN
        GPIO.output(self.request_pin, Secondary.NOT_SHUTDOWN_REQUEST)
        self._request_status = Secondary.NOT_SHUTDOWN_REQUEST
