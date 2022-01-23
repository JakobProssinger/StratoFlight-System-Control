"""
@File:          ina260.py
@Descrption:    module to read INA260 
@Author:        Prossinger Jakob
@Date:          23 January 2022
@Todo:          * add logging
"""
from sensor import sensor
from sensor.sensor_data import sensor_data

_INA260_DEFAULT_DEVICE_ADDRESS = 0x40
_INA260_CONFIG_ADDR = 0x00
_INA260_CURRENT_ADDR = 0x01
_INA260_BUS_VOLTAGE_ADDR = 0x02
_INA260_BUS_VOLTAGE_LSB = 1.25  # mV
_INA260_CURRENT_LSB = 1.25  # mA


class INA260(sensor.Sensor):
    __DATA_NAMES = ["Voltage", "Current"]
    __DATA_UNITS = ["mV", "mA"]

    def __init__(self, name: str, address: int):
        self.name = name
        self.sensor_type = sensor._SENSOR_TYPE[sensor._INA260]
        self.i2c = smbus.SMBus(1)  # /dev/i2c-1
        self.device_address = address
        self.data = sensor_data.sensor_data(
            INA260.__DATA_NAMES,
            [0.0, 0.0], INA260.__DATA_UNITS, 2)

    def read_Sensor(self):
        self.data.data_value = [self.get_bus_voltage(), self.get_current()]

    def get_Data(self):
        return self.data

    def twos_compliment_to_int(self, val: int, len: int) -> int:
        # Convert twos compliment to integer
        if (val & (1 << len - 1)):
            val = val - (1 << len)
        return val

    def read_ina(self, register_address: int, register_size: int) -> float:
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
        raw_read = self.read_ina(self._INA260_BUS_VOLTAGE_ADDR, 2)
        if type(raw_read[0]) != int:
            return "noVoltage"
        word_rdata = raw_read[0] * 256 + raw_read[1]
        voltage = round(float(word_rdata) * self._INA260_BUS_VOLTAGE_LSB, 3)
        return voltage

    def get_current(self) -> float:
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
        byte_list = [0x80, 0x00]  # reset code for INA260
        self.write_ina(self._INA260_CONFIG_ADDR, byte_list)

    def read_configuration_register(self) -> int:
        return self.read_ina(self._INA260_CONFIG_ADDR, 2)

    def activate_average(self, samples: int) -> None:
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
            print("actiavted average, Samples : " + str(samples) +
                  " on INA260 with I2C-Address: " +
                  str(hex(self.device_address)))
