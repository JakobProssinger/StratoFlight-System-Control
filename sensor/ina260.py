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
        # self.i2c = smbus.SMBus(1)  # /dev/i2c-1
        self.device_address = address
        self.data = sensor_data.sensor_data(
            INA260.__DATA_NAMES,
            [0.0, 0.0], INA260.__DATA_UNITS, 2)

    def read_Sensor(self):
        return ["Voltage", "Current"]

    def get_Data(self):
        return self.data
