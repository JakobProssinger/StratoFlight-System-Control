import serial
from time import sleep
from sensor.neo6m import NEO6M


def read_neo6m() -> None:
    gps_sensor = NEO6M("GPS Sensor")

    while 1:
        gps_sensor.read_Sensor()
        print(gps_sensor.get_Data())
        sleep(10)


if __name__ == '__main__':
    read_neo6m()
