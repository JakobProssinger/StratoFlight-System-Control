"""
@File:          ina260.py
@Descrption:    a module read and write data from the Adafruit INA260 chip
@Author:        Prossinger Jakob
@Date:          14 December 2021
@Todo:          * translate the read config register
"""
from typing import Sized
import smbus
import logging

# setup for logging
ina_module_logger = logging.getLogger("strato_logger.sensor_process.INA260")


#source: https://github.com/charkster/INA260/tree/077521eded5c8efe22bf843dfd2fa462e10bb9c5
class INA260:
    """
    A class used to read and write data from the Adafruit
    Ina260 chip

    ...

    Attributes
    ----------
    self.i2c : smbus
        opens a i2c bus for the INA260

    self.device_address : int (hex)
        I2C Address of the INA260
    
    self.logger : logger
        logger of the ina260

    ina_module_logger : Logger
        a logger from the standard logger module. Child logger from strato_logger

    _INA260_DEFAULT_DEVICE_ADDRESS: int (hex)
        Default Address of the Adafruit INA260.

    _INA260_CONFIG_ADDR : int(hex)
        Address of the config register of the Adafruit INA260.

    _INA260_CURRENT_ADDR : int (hex)
        Address of the electrical current register of the Adafruit INA260.

    _INA260_BUS_VOLTAGE_ADDR : int (hex)
        Address of the electrical voltage register of the Adafruit INA260.

    _INA260_BUS_VOLTAGE_LSB : double
        voltage size of the least significant bit of the voltage register
        of the Adafruit INA260, in mV.

    _INA260_CURRENT_LSB : double
        electrical current size of the least significant of the current register 
        bit of the Adafruit INA260, in mA

    Methods
    -------
    twos_compliment_to_int(self, val: int, len: int) -> int
        returns the integer of a twos_compilemt number, based on the legth.
    
    read_ina(self, register_address: int, register_size: int) -> float
        returns the values from an INA260 register
    
    write_ina(self, register_address: int, byte_list: int) -> bool
        writes a list of bytes on an INA260-Address.
        If succesful return true

    get_bus_voltage(self) -> float
        reads and returns the voltage from the voltage register in
        the INA260 object. If successful return a float int mV else return "noVoltage"

    get_current(self) -> float
        reads and returns the current from the current register in
        the INA260 object. If successful return a float in mA else return "noCurrent"
    
    reset_chip() -> None
        resets the config register of the INA260 to default.

    read_configuration_register(self) -> int:
        reads and returns the configregister of the INA260

    def activate_average(self, samples: int) -> None:
        activates the averaging on the INA260 based on the samples.
    """

    _INA260_DEFAULT_DEVICE_ADDRESS = 0x40
    _INA260_CONFIG_ADDR = 0x00
    _INA260_CURRENT_ADDR = 0x01
    _INA260_BUS_VOLTAGE_ADDR = 0x02
    _INA260_BUS_VOLTAGE_LSB = 1.25  #mV
    _INA260_CURRENT_LSB = 1.25  #mA

    # Constructor
    def __init__(self,
                 device_address: int = _INA260_DEFAULT_DEVICE_ADDRESS) -> None:
        """
        Parameters
        ----------
        device_address : int (hex)
            the i2c address of the INA260 
        """

        self.i2c = smbus.SMBus(1)  #/dev/i2c-1
        self.device_address: int = device_address
        self.logger = logging.getLogger(
            "strato_logger.sensor_process.ina260.INA260")
        self.logger.info("created ina260 object")

    def twos_compliment_to_int(self, val: int, len: int) -> int:
        """
        Description
        ----------
        returns the integer of a twos_compilemt number, based on the legth.

        Parameters
        ----------
        val : int 
            integer value of a tows compliment number 
        
        len : int
            length of the integer number         
        """
        # Convert twos compliment to integer
        if (val & (1 << len - 1)):
            val = val - (1 << len)
        return val

    def read_ina(self, register_address: int, register_size: int) -> float:
        """
        Description
        ----------
        returns the values from an INA260 register

        Parameters
        ----------
        register_address : int 
            integer value of the i2c address  
        
        register_size : int
            size of the register in bytes

        Throws
        ------
        OSException:
            if no I2C could could be made.

        Exception:
            if something else happends.
        """
        try:
            return self.i2c.read_i2c_block_data(self.device_address,
                                                register_address,
                                                register_size)
        except OSError:
            self.logger.error("Could not read from INA260 with I2C-Address: " +
                              str(hex(self.device_address)))
        except Exception as e:
            self.logger.error("Exception on INA260 with I2C-Address: " +
                              str(hex(self.device_address)))
        return ["Error"] * register_size

    def write_ina(self, register_address: int, byte_list: int) -> bool:
        """
        Description
        ----------
        writes a list of bytes on an INA260-Address.
        If succesful return true

        Parameters
        ----------
        register_address : int 
            integer value of the i2c address  
        
        byte_list : int
            integer list with bytes to write on the i2c address

        Throws
        ------
        OSException:
            if no I2C could could be made.

        Exception:
            if something else happends.
        """
        try:
            self.i2c.write_i2c_block_data(self.device_address,
                                          register_address, byte_list)
        except OSError:
            self.logger.error("Could not write to INA260 with I2C-Address: " +
                              str(hex(self.device_address)))
            return False
        except Exception as e:
            self.logger.error("Exception on INA260 with I2C-Address: " +
                              str(hex(self.device_address)))
            return False
        return True

    def get_bus_voltage(self) -> float:
        """
        Description
        ----------
        reads and returns the voltage from the voltage register in
        the INA260 object. If successful return a float int mV else return "noVoltage"
        """
        raw_read = self.read_ina(self._INA260_BUS_VOLTAGE_ADDR, 2)
        if type(raw_read[0]) != int:
            return "noVoltage"
        word_rdata = raw_read[0] * 256 + raw_read[1]
        vbus = round(float(word_rdata) * self._INA260_BUS_VOLTAGE_LSB, 3)
        return vbus

    def get_current(self) -> float:
        """
        reads and returns the current from the current register in
        the INA260 object. If successful return a float in mA else return "noCurrent"
        """
        raw_read = self.read_ina(self._INA260_CURRENT_ADDR, 2)
        if type(raw_read[0]) != int:
            return "noCurrent"
        word_rdata = raw_read[0] * 256 + raw_read[1]
        current_twos_compliment = word_rdata
        current_sign_bit = current_twos_compliment >> 15
        if (current_sign_bit == 1):
            current = float(
                self.twos_compliment_to_int(current_twos_compliment,
                                            16)) * self._INA260_CURRENT_LSB
        else:
            current = float(current_twos_compliment) * self._INA260_CURRENT_LSB
        return current

    def reset_chip(self) -> None:
        """
        resets the config register of the INA260 to default.
        """
        byte_list = [0x80, 0x00]  # reset code for INA260
        self.write_ina(self._INA260_CONFIG_ADDR, byte_list)

    def read_configuration_register(self) -> int:
        """
        reads and returns the configregister of the INA260
        """
        return self.read_ina(self._INA260_CONFIG_ADDR, 2)

    def activate_average(self, samples: int) -> None:
        """
        Description
        ----------
        activates the averaging on the INA260 based on the samples.

        Parameters
        ----------
        samples : int 
            sampels to average
        """
        byte_list = [0x61, 0x27]
        switch = {
            1: 0x061 + (0b000 << 1),
            4: 0x061 + (0b001 << 1),
            16: 0x061 + (0b010 << 1),
            64: 0x061 + (0b011 << 1),
            128: 0x061 + (0b100 << 1),
            256: 0x061 + (0b101 << 1),
            512: 0x061 + (0b110 << 1),
            1024: 0x061 + (0b111 << 1)
        }
        byte_list[0] = switch.get(samples, 0x61)
        if self.write_ina(self._INA260_CONFIG_ADDR, byte_list) is True:
            self.logger.info("actiavted average, Samples : " + str(samples) +
                             " on INA260 with I2C-Address: " +
                             str(hex(self.device_address)))