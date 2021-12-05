import os
import logging

logger = logging.getLogger("strato_logger.cpu_temperature_sensor")
logger.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s - %(name)-12s - %(levelname)s:\n\tat %(funcName)s() - %(message)s'
)
file_Handler = logging.FileHandler('./Logging-Files/sensor_data.csv')
file_Handler.setLevel(logging.ERROR)
file_Handler.setFormatter(formatter)
logger.addHandler(file_Handler)


def get_raspberry_temperature() -> float:
    try:
        cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
        return cpu_temp.replace("temp=", "")
    except Exception as e:
        logger.error("couldnt read CPU Temperature")
    return "noCPUTemperature"