"""
@File:          neo6m.py
@Descrption:    module to read Neo-6M GPS Sensor
@Author:        Prossinger Jakob
@Date:          23 February 2022
@Todo:          * implement altitude
                * define units
"""
import serial
import os
import pynmea2
import sensor
from sensor import sensor
from sensor.sensor_data import sensor_data


class NEO6M(sensor.Sensor):
    """
    class to handle read of the neo-6m GPS sensor
    child class of sensor.Sensor

    Attributes:
        __NEO6M_DEFAULT_Directory (str): default directory to the neo6m data directory

        __DATA_NAMES (list): stores the names for the data points of the neo6m

        __DATA_UNITS (list): stores the units for the data point of the neo6m 

    """
    __NEO6M_DEFAULT_Directory = "/dev/ttyAMA0"
    __DATA_NAMES = ["Longitude", "Latitude", "Altitude"]
    __DATA_UNITS = ["", "", "meter"]  # [1] [2] empty because they can change

    def __init__(self, name: str, directory: str = __NEO6M_DEFAULT_Directory) -> None:
        """
        init function of neo6m

        Args:
            name (str): name of the neo6m sensor
            directory (str): directory to the neo6m data directory. Defaults to __NEO6M_DEFAULT_Directory.
        """
        self.name = name
        self.directory = directory
        self.data = sensor_data.sensor_data(
            NEO6M.__DATA_NAMES,
            [0.0, 0.0, 0.0], NEO6M.__DATA_UNITS, 3)

    def read_Sensor(self) -> list:
        """
        reading longitude latitude and altitude from the neo6m data directory

        Returns:
            list: return lat. long. and alt. in a list if sensor was found otherwise it will return a list with three - 
        """
        try:
            ser = serial.Serial(self.directory, baudrate=9600, timeout=0.2)
            for i in range(0, 10):
                newdata = ser.readline()
                if str(newdata[0:6]) == "b'$GPGGA'":
                    newmsg = pynmea2.parse(str(newdata)[2:-5])
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    alt = newmsg.altitude
                    ser.close()
                    self.data.data_value = [f'{lat} {str(newmsg.lat_dir)}', f'{lng} {str(newmsg.lon_dir)}', alt]
                    return
        except KeyboardInterrupt:
            ser.close()
        except Exception as e:
            ser.close()
            print(e)
        finally:
            ser.close()
        self.data.data_value = ["-", "-", "-"]  # TODO ADD Error code

    def get_Data(self) -> sensor_data.sensor_data:
        """
        gets the data fom the neo6m

        Returns:
            sensor_data.sensor_data: data parameter of the neo6m  
        """
        return self.data
