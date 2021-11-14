import os


def get_raspberry_temperature():
    cpu_temp = os.popen("vcgencmd measure_temp").readline()[:-3]
    return cpu_temp.replace("temp=", "")