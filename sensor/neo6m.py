"""
@File:          neo6m.py
@Descrption:    module to read Neo-6M GPS Sensor
@Author:        Prossinger Jakob
@Date:          23 January 2021
@Todo:          * implement real sensor readin
                * implement altitude
"""
import serial
import os
import pynmea2
import sensor
from sensor import sensor
from sensor.sensor_data import sensor_data

_NEO6M_DEFAULT_Directory = "/dev/ttyAMA0"


class NEO6M(sensor.Sensor):
    __DATA_NAMES = ["Longitude", "Latitude", "Altitude"]
    __DATA_UNITS = ["tbd", "tbd", "tbd"]

    def __init__(self, name: str, directory: str = _NEO6M_DEFAULT_Directory) -> None:
        # self.sensor_type = _SENSOR_TYPE[_NEO6M]
        self.name = name
        self.directory = directory
        self.data = sensor_data.sensor_data(
            NEO6M.__DATA_NAMES,
            [0.0, 0.0, 0.0], NEO6M.__DATA_UNITS, 3)

    def read_Sensor(self) -> list:
        try:
            ser = serial.Serial(self.directory, baudrate=9600, timeout=0.2)
            for i in range(0, 10):
                newdata = ser.readline()
                if str(newdata[0:6]) == "b'$GPRMC'":
                    newmsg = pynmea2.parse(str(newdata)[2:-5])
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    gps = " Latitude = " + \
                        str(lat) + " and Longitude = " + str(lng)
                    ser.close()
                    return [lat, lng, 0.0]  # TODO Add longitude
        except KeyboardInterrupt:
            ser.close()
        except Exception as e:
            ser.close()
            print(e)
        finally:
            ser.close()
        return ["-", "-", "-"]  # TODO ADD Error code

    def get_Data(self) -> sensor_data.sensor_data:
        return self.data
