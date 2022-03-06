# main controll system for StratoFlight 2021/22

## Project Setup

### Clone Repository into:
```
/home/pi/Documents/
```
```
git clone https://github.com/JakobProssinger/StratoFlight-System-Control.git
```
### install python packets
    
### Activate I2C, SPI, RX-TX, 1-Wire
See guide in at https://pinout.xyz/

### Activate UART for NEO-6M
See guide at: https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
```
sudo nano /boot/config.txt
```
Append following files:
```
dtparam=spi=on
dtoverlay=pi3-disable-bt
#core_freq=250
enable_uart=1
force_turbo=1
```
In 
```
sudo nano /boot/cmdline.txt
```
replace with:
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
Test the sensor with by reading the following file. If file is empty sensor was not found.
```
sudo cat /dev/ttyAMA0
```

### Activate DHT22
Install pigpio with pip3
```
sudo pip3 install pigpio
```
Autostart the pigpio deamon on Raspberry Pi boot:
add the following line in /etc/rc.local before line "exit 0"
```
sudo pigpiod
```

### Setup Flask
Start falsk server in /Documents/StratoFlight-System-Control
```
sudo python3 app.py
```



### Autostart webserver
The bestway to start autostart the flask is by using a linux service.
To create the service create the following file:
```
sudo nano /etc/systemd/system/strato-flight.service
```
```
[Unit]
Description=Strato Flight
[Install]
WantedBy=multi-user.target
[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/Documents/StratoFlight-System-Control/app.py
Restart=always
TimeoutSec=30 
```
You can now start the service with the following command:
```
sudo systemctl start strato-flight
```
Now check the functionality of the service with:
```
sudo systemctl status strato-flight
```
If the server started correctly, enable the service:
```
sudo systemctl enable strato-flight
```


## StratoFlight-System-Control

### Test-System
| Name                          | Usage                                                 |
| ---                           | ---                                                   |
| Raspberry Pi Model 4B         | Power source, reading Sensors with I2C, RX-TX, 1-Wire | 
| AdaFruit INA260               | Voltage and Current Measurement                       |
| NEO6M                         | GPS sensor with UART Interface                        |
| DHT22                         | Temperature and relative Humidity                     | 

#### Raspberry Pi Used Pinout
| Pin # | Cable Colour | Name          | Usage                             |
| ---   | ---          | ---           | ---                               |
| 02    | RED          | 5V DC-Power   | Power for INA260                  |
| 03    | BROWN        | SDA1 (I2C)    | SDA for I2C network               |
| 05    | BLUE         | SCL1 (I2C)    | SCL for I2C network               |
| 10    | YELLOW       | RX (UART)     | reading from GPS Neo-6M           |
| 11    | GREEN        | GPIO          | case LED green                    |
| 13    | WHITE        | GPIO          | case LED red                      |
| 16    | VIOLET       | 1-Wire        | reading DHT22                     |
| 39    | BLACK        | Ground        | GND                               |

#### Python-Packages
| Name                                                                    | Usage                                                       |
| ---                                                                     | ---                                                         |
| flask                                                                   | Hosting the webserver for system-Control and user access    |
| threading                                                               | threading starting and stopping threads                     |
| logging                                                                 | logging error messages and debug inforamtion                |
| RPi.GPIO                                                                | Controling GPIO Pins and case LEDs                          |
| atexit                                                                  | handling of crashes or programm shutdowns                   |
| smbus                                                                   | I2C handling                                                |
| os                                                                      | opening local files                                         |
| csv                                                                     | handling formatting of csv files                            | 
| pynmea2                                                                 | compling the GPS Neo-6M data                                |
| serial                                                                  | reading GPS Neo-6M                                          |
| pigpio                                                                  | Sensor library of DHT22                                     |
| waitress                                                                | serving flask production server                             |

***

### Flying-System
| Name                          | Usage                                                 |
| ---                           | ---                                                   |
| Raspberry PI Model 0          | Power source, reading Sensors with I2C, RX-TX, 1-Wir  | 
| AdaFruit INA260               | Voltage and Current Measurement                       |
| NEO6M                         | GPS sensor with UART Interface                        |
| DHT22                         | Temperature and relative Humidity                     | 
***
