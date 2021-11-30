from typing import Sized
import smbus
import logging

# setup for logging
ina_module_logger = logging.getLogger("strato_logger.sensor_process.ina260")


#source: https://github.com/charkster/INA260/tree/077521eded5c8efe22bf843dfd2fa462e10bb9c5
class INA260:

    _INA260_DEFAULT_DEVICE_ADDRESS = 0x40
    _INA260_CONFIG_ADDR = 0x00
    _INA260_CURRENT_ADDR = 0x01
    _INA260_BUS_VOLTAGE_ADDR = 0x02
    _INA260_BUS_VOLTAGE_LSB = 1.25  #mV
    _INA260_CURRENT_LSB = 1.25  #mA

    # Constructor
    def __init__(self,
                 device_address: int = _INA260_DEFAULT_DEVICE_ADDRESS) -> None:
        self.i2c = smbus.SMBus(1)  #/dev/i2c-1
        self.device_address: int = device_address
        self.logger = logging.getLogger(
            "strato_logger.sensor_process.ina260.Ina260")

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
            self.logger.error("Could not read from INA260 with I2C-Address: " +
                              str(hex(self.device_address)))
        except Exception as e:
            self.logger.error("Exception on INA260 with I2C-Address: " +
                              str(hex(self.device_address)))
        return ["Error"] * register_size

    def write_ina(self, register_address: int, byte_list: int) -> bool:
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
        raw_read = self.read_ina(self._INA260_BUS_VOLTAGE_ADDR, 2)
        if type(raw_read[0]) != int:
            return "noVoltage"
        word_rdata = raw_read[0] * 256 + raw_read[1]
        vbus = round(float(word_rdata) * self._INA260_BUS_VOLTAGE_LSB, 3)
        return vbus

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
            self.logger.info("actiavted average, Samples : " + str(samples) +
                             " on INA260 with I2C-Address: " +
                             str(hex(self.device_address)))