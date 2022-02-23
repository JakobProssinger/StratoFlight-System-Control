"""
@File:          ina260.py
@Descrption:    module to read INA260 
@Author:        Prossinger Jakob
@Date:          23 February 2022
@Todo:          * add logging
"""
from sensor import sensor
from sensor.sensor_data import sensor_data
import smbus

_INA260_DEFAULT_DEVICE_ADDRESS = 0x40
_INA260_CONFIG_ADDR = 0x00
_INA260_CURRENT_ADDR = 0x01
_INA260_BUS_VOLTAGE_ADDR = 0x02
_INA260_BUS_VOLTAGE_LSB = 1.25  # mV
_INA260_CURRENT_LSB = 1.25  # mA


class INA260(sensor.Sensor):
    """
    class to reading INA260 sensor

    Attributes:
        __DATA_NAMES (list): stores the names for the data points of the ina260

        __DATA_UNITS (list): stores the units for the data point of the ina260

    """
    __DATA_NAMES = ["Voltage", "Voltage-Average", "Current"]
    __DATA_UNITS = ["mV", "mV", "mA"]

    def __init__(self, name: str, address: int = _INA260_DEFAULT_DEVICE_ADDRESS) -> None:
        """
        init function of ina260

        Args:
            name (str): name of the sensor
            address (int, optional): address of the INA260. Defaults to _INA260_DEFAULT_DEVICE_ADDRESS.
        """
        self.name = name
        self.sensor_type = sensor._SENSOR_TYPE[sensor._INA260]
        self.i2c = smbus.SMBus(1)  # /dev/i2c-1
        self.device_address = address
        self.data = sensor_data.sensor_data(
            INA260.__DATA_NAMES,
            [0.0, 0.0], INA260.__DATA_UNITS, 3)
        self.voltage_fifo = []
        self.reset_chip()

    def read_Sensor(self) -> None:
        """
        read data of the ina260 and store it in self.data object
        """
        self.data.data_value = [self.get_bus_voltage(
        ), self.get_voltage_average(), self.get_current()]

    def get_Data(self) -> sensor_data.sensor_data:
        """
        return data object of the ina260 instance

        Returns:
            sensor_data.sensor_data: ina260 data
        """
        return self.data

    def twos_compliment_to_int(self, num: int, len: int) -> int:
        """
        calculate the twos compliment of a number with a given length

        Args:
            num (int): number to convert
            len (int): length of the the number

        Returns:
            int: twos compliment of the number
        """
        if (num & (1 << len - 1)):
            num = num - (1 << len)
        return num

    def read_ina(self, register_address: int, register_size: int) -> list:
        """
        read from a {register_address} of the ina260

        Args:
            register_address (int): I2C-Address of an ina260 register
            register_size (int): size of the register in byte

        Returns:
            list: bytes from the ina260 register. If sensor was not found 
                    return ["Error"] * {register_size} 
        """
        try:
            return self.i2c.read_i2c_block_data(self.device_address,
                                                register_address,
                                                register_size)
        except OSError:
            print("Could not read from INA260 with I2C-Address: " +
                  str(hex(self.device_address)))
        except Exception as e:
            print("Exception on INA260 with I2C-Address: " +
                  str(hex(self.device_address)))
        return ["Error"] * register_size

    def write_ina(self, register_address: int, byte_list: int) -> bool:
        """
        write the a list of bytes to the ina260 {register_address}

        Args:
            register_address (int): I2C register of the INA260
            byte_list (int): list of bytes to write into  the I2C register

        Returns:
            bool: True if sensor was read, else False
        """
        try:
            self.i2c.write_i2c_block_data(self.device_address,
                                          register_address, byte_list)
        except OSError:
            print("Could not write to INA260 with I2C-Address: " +
                  str(hex(self.device_address)))
            return False
        except Exception as e:
            print("Exception on INA260 with I2C-Address: " +
                  str(hex(self.device_address)))
            return False
        return True

    def get_bus_voltage(self) -> float:
        """
        read voltage from the ina260 instance

        Returns:
            float: voltage of the ina260 in mV. If not found return noVoltage
        """
        raw_read = self.read_ina(_INA260_BUS_VOLTAGE_ADDR, 2)
        if type(raw_read[0]) != int:
            self.voltage_fifo.insert(0, "noVoltage")
            if len(self.voltage_fifo) > 5:
                self.voltage_fifo.pop()
            return "noVoltage"
        word_rdata = raw_read[0] * 256 + raw_read[1]
        voltage = round(float(word_rdata) * _INA260_BUS_VOLTAGE_LSB, 3)
        self.voltage_fifo.insert(0, voltage)
        if len(self.voltage_fifo) > 5:
            self.voltage_fifo.pop()
        return voltage

    def get_voltage_average(self) -> float:
        sum = 0.0
        float_len = 0  # amount of all elements with type float
        for value in self.voltage_fifo:
            if type(value) != float:
                continue
            float_len += 1
            sum += value
        if float_len == 0:
            return "noFound"  # TODO ADD ERROR CODE
        return sum / float_len

    def get_current(self) -> float:
        """
        read current from the ina260 instance

        Returns:
            float: current of the ina260 in mV. If not found return noCurrent
        """
        raw_read = self.read_ina(_INA260_CURRENT_ADDR, 2)
        if type(raw_read[0]) != int:
            return "noCurrent"
        word_rdata = raw_read[0] * 256 + raw_read[1]
        current_twos_compliment = word_rdata
        current_sign_bit = current_twos_compliment >> 15
        if (current_sign_bit == 1):
            current = float(
                self.twos_compliment_to_int(current_twos_compliment,
                                            16)) * _INA260_CURRENT_LSB
        else:
            current = float(current_twos_compliment) * _INA260_CURRENT_LSB
        return current

    def reset_chip(self) -> None:
        """
        write the reset command to the ina260
        """
        byte_list = [0x80, 0x00]  # reset code for INA260
        self.write_ina(_INA260_CONFIG_ADDR, byte_list)

    def read_configuration_register(self) -> int:
        """
        read configure register from the ina260 I2C register

        Returns:
            int: list of the configure register
        """
        return self.read_ina(_INA260_CONFIG_ADDR, 2)

    def activate_average(self, samples: int) -> None:
        """
        activate averaging of the INA260 sensor data

        Args:
            samples (int): samples to average 
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
        if self.write_ina(_INA260_CONFIG_ADDR, byte_list) is True:
            print("actiavted average, Samples : " + str(samples) +
                  " on INA260 with I2C-Address: " +
                  str(hex(self.device_address)))
