"""
@File:          secondary.py
@Descrption:    
@Author:        Prossinger Jakob
@Date:          22 February 2022
@Todo:          * 
"""
import RPi.GPIO as GPIO


class Secondary():
    __SHUTDOWN_REQUEST = GPIO.HIGH
    __NOT_SHUTDOWN_REQUEST = GPIO.LOW

    __SHUTDOWN = GPIO.LOW
    __NOT_SHUTDOWN = GPIO.HIGH

    def __init__(self, raspberry_name: str, request_pin: int,
                 shutdown_pin: int, ina260_name):
        self.name: str = raspberry_name
        self.request_pin: int = request_pin
        self.shutdown_pin: int = shutdown_pin
        self.__request_status: bool = __NOT_SHUTDOWN_REQUEST
        self.__shutdown_status: bool = __NOT_SHUTDOWN

    def get_Name(self) -> str:
        return self.name

    def request_shutdown(self) -> None:
        GPIO.output(self.raspberry_pin, __SHUTDOWN_REQUEST)
        self.request_status = __SHUTDOWN_REQUEST

    def shutdown(self) -> None:
        GPIO.output(self.shutdown_pin, __SHUTDOWN)
        self.shutdown_status = __SHUTDOWN

    def boot(self) -> None:
        GPIO.output(self.shutdown_pin, __NOT_SHUTDOWN)
        GPIO.output(self.request_pin, __NOT_SHUTDOWN_REQUEST)
