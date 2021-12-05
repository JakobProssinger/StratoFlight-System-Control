from src.logging.csv_handler import CSVHandler
from src.sensors.sensor_process import SensorObject
import time

CSV_DIRECTORY = './Logging-Files/sensor_data.csv'
TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]
HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'ds18b28 Temperature', 'raspberry temperature'
]


def main() -> None:
    csv_handler = CSVHandler(CSV_DIRECTORY, HEADER_LIST)
    csv_handler.csv_write_data_row(HEADER_LIST)
    sensors_processor = SensorObject(INA260_DEVICE_ADDRESSES,
                                     TEMPSENSORS_DEVICE_ADDRESSES, csv_handler)
    while 1:
        sensors_processor.system_process()
        print("cycle ended")
        time.sleep(1)


if __name__ == "__main__":
    print("Programm Started")
    main()