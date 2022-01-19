"""
@File:          07_NEO-6M.py
@Descrption:    starts flask server for Strato Flight 2021/2022
@Author:        Prossinger Jakob
@Date:          19 January 2021
@Todo:          * 
"""
import serial
import pynmea2
import atexit
import os

port = "/dev/ttyAMA0"


'''
*Anmkerungen: ohne Antenne beides 0                                                                                                                                                                                                                                                                                                                                                                           
'''


@atexit.register
def atexit_function() -> None:
    # ser.close()
    print("closed")


def read_NEO6M() -> list:
    ser = serial.Serial(port, baudrate=9600, timeout=0.2)
    #dataout = pynmea2.NMEAStreamReader()
    try:
        for i in range(0, 10):
            print(i)

            newdata = ser.readline()
            if str(newdata[0:6]) == "b'$GPRMC'":
                newmsg = pynmea2.parse(str(newdata)[2:-5])
                lat = newmsg.latitude
                lng = newmsg.longitude
                gps = " Latitude = " + \
                    str(lat) + " and Longitude = " + str(lng)
                ser.close()
                return [lat, lng]
    except KeyboardInterrupt:
        ser.close()
        print("closed")
    except Exception as e:
        ser.close()
        print(e)
    ser.close()
    return [0, 0]


def main():
    print(read_NEO6M())
    print("-" * 20)
    print(read_NEO6M())


if __name__ == "__main__":
    main()
