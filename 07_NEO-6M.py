import serial
import time
import string
import pynmea2
import atexit

port = "/dev/ttyAMA0"


'''
*Anmkerungen: ohne Antenne beides 0                                                                                                                                                                                                                                                                                                                                                                           
'''
@atexit.register
def atexit_function() -> None:
    ser.close()
    print("closed")

ser = serial.Serial(port, baudrate=9600, timeout=0.5)

try:
    while True:
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()
        #print(str(newdata[0:6]))
        if str(newdata[0:6]) == "b'$GPRMC'":
            newmsg = pynmea2.parse(str(newdata)[2:-5])
            lat = newmsg.latitude
            lng = newmsg.longitude
            gps = str(time.asctime()) +"  Latitude=" + str(lat) + " and Longitude = " 
            + str(lng)                                             
            print(gps)
       # ser.close()
except KeyboardInterrupt:
    ser.close()
    ser.exit()
    print("closed")