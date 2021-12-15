"""
@File:          internal.py
@Descrption:    a module to hantel internal data from raspberry
@Author:        Prossinger Jakob
@Date:          15 December 2021
@Todo:          * 
"""
import os
import logging

logger = logging.getLogger("strato_logger.internal")
"""
A class used to Handle csv file writing and formatting 

...

Attributes
----------
ina_module_logger : Logger
    alogger from the standard logger module. Child logger from strato_logger

Methods
-------
get_raspberry_temperature() -> float
    returns the CPU temperature of the raspberry.
"""


def get_raspberry_temperature() -> float:
    """"
    Description
    -----------

        returns the CPU temperature of the raspberry in °C as float. 
        If not succesful returs a string with "noCPUTemperature"

    Throws
    ------
    Exception:
        if temperature couldnt be read.
    
    """
    try:
        cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
        return cpu_temp.replace("temp=", "")
    except Exception as e:
        logger.error("couldnt read CPU Temperature")
    return "noCPUTemperature"