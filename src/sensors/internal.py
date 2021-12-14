import os
import logging

logger = logging.getLogger("strato_logger.cpu_temperature_sensor")


def get_raspberry_temperature() -> float:
    try:
        cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
        return cpu_temp.replace("temp=", "")
    except Exception as e:
        logger.error("couldnt read CPU Temperature")
    return "noCPUTemperature"