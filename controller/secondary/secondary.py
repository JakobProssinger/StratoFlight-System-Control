"""
@File:          secondary.py
@Descrption:    
@Author:        Prossinger Jakob
@Date:          11 April 2022
@Todo:          * 
"""
import RPi.GPIO as GPIO


class Secondary():
    SHUTDOWN_REQUEST = GPIO.HIGH
    NOT_SHUTDOWN_REQUEST = GPIO.LOW

    SHUTDOWN = GPIO.LOW
    NOT_SHUTDOWN = GPIO.HIGH

    def __init__(self, raspberry_name: str, request_shutdown_pin: int,
                 power_off_pin: int, shutdown_voltage: float, power_on_voltage: float):
        self.name: str = raspberry_name
        # GPIO on primary connected with secondary gpio
        self.request_shutdown_pin: int = request_shutdown_pin
        # GPIO on primary connected with Secondary voltage controller
        self.power_off_pin: int = power_off_pin
        self._request_status: bool = Secondary.NOT_SHUTDOWN_REQUEST
        self._power_status: bool = Secondary.NOT_SHUTDOWN
        # threshold to shudown secondary
        self.shutdown_voltage: float = shutdown_voltage
        # threshold to trun on secondary after shutdown
        self.power_on_voltage: float = power_on_voltage
        self.turn_on()

    def get_Name(self) -> str:
        return self.name

    def get_Power_status(self) -> bool:
        return self._power_status

    def get_Request_status(self) -> bool:
        return self._request_status

    def get_Shutdown_voltage(self) -> float:
        return self.shutdown_voltage

    def get_Power_on_voltage(self) -> float:
        return self.power_on_voltage

    def request_shutdown(self) -> None:
        '''
        primary requests the secondary to shutdown by sending a
        shutdown signal with the gpio pin defined in {self.request_shutdown_pin}
        '''
        GPIO.output(self.request_shutdown_pin, Secondary.SHUTDOWN_REQUEST)
        self._request_status = Secondary.SHUTDOWN_REQUEST

    def shutdown(self) -> None:
        '''
        turns off the power of the secondary
        '''
        GPIO.output(self.power_off_pin, Secondary.SHUTDOWN)
        self._power_status = Secondary.SHUTDOWN

    def turn_on(self) -> None:
        '''
        turns on the power of the secondary 
        '''
        GPIO.output(self.power_off_pin, Secondary.NOT_SHUTDOWN)
        self._power_status = Secondary.NOT_SHUTDOWN
        GPIO.output(self.request_shutdown_pin, Secondary.NOT_SHUTDOWN_REQUEST)
        self._request_status = Secondary.NOT_SHUTDOWN_REQUEST
