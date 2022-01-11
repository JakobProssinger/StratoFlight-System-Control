import serial
import time
import string
import pynmea2

port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout = pynmea2.NMEAStreamReader()
try:
    while True:
        newdata = ser.readline()
        if newdata[0:6] == b'$GPRMC':
            try:

                newmsg = pynmea2.parse(str(newdata))
                lat = newmsg.latitude
                lng = newmsg.longitude
                gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
                print(gps)
            except Exception as e:
                print("ERROR: No Signal")
except KeyboardInterrupt:
    ser.close()
    print("closed")