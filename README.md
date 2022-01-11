# main controll system for StratoFlight 2021/22

## Project Setup

### Clone Repository into:
```
/home/pi/Documents/
```
```
git clone https://github.com/JakobProssinger/StratoFlight-System-Control.git
```
### Activate I2C, SPI, RX-TX, 1-Wire
See guide in at https://pinout.xyz/

### Activate UART
See guide at: https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
```
sudo nano /boot/config.txt
```
Append following files:
```
dtparam=spi=on
dtoverlay=pi3-disable-bt
core_freq=250
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
Test function:
```
sudo cat /dev/ttyAMA0
```

### Setup Flask

```
export FLASK_APP=app
```

## StratoFlight-System-Control

### Test-System
| Name                          | Usage                                                |
| ---                           | ---                                                  |
| Raspberry Pi Model 4         | Power source, reading Sensors with I2C, SPI, 1-Wire  | 
| AdaFruit INA260               | Voltage and Current Measurement                      |

#### Raspberry Pi Used Pinout
| Pin # | Cable Colour | Name          | Usage                             |
| ---   | ---          | ---           | ---                               |
| 02    | RED          | 5V DC-Power   | Power for INA260                  |
| 03    | BROWN        | SDA1 (I2C)    | SDA for I2C network               |
| 05    | BLUE         | SCL1 (I2C)    | SCL for I2C network               |
| 11    | GREEN        | GPIO          | case LED green                    |
| 13    | WHITE        | GPIO          | case LED red                      |
| 39    | BLACK        | Ground        | GND                               |

#### Python-Packages
| Name                                                                    | Usage                                      |
| ---                                                                     | ---                                        |
| flask                                                                   | Hosting the webserver for system-Control and user access   |
| threading                                                               | threading starting and stopping threads    |
| logging                                                                 | logging error messages and debug inforamtion|
| RPi.GPIO                                                                | Controling GPIO Pins and case LEDs |
| atexit                                                                  | handling of crashes or programm shutdowns |
| smbus                                                                   | I2C handling|
| os                                                                      | opening local files |
| csv                                                                     | handling formatting of csv files | 

***

### Flying-System
| Name                          | Usage                                                |
| ---                           | ---                                                  |
| Raspberry PI Model 0         | Power source, reading Sensors with I2C, SPI, 1-Wire  | 
| AdaFruit INA260               | Voltage and Current Measurement                      |
***
