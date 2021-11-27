import csv
from src.logging.csv_handler import CSV_HANDLER
from src.sensors.sensor_process import sensor_data_object, sensor_object
import time, datetime

CSV_DIRECTORY = './Logging-Files/sensor_data.csv'
TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]
HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'ds18b28 Temperature', 'raspberry temperature'
]

if __name__ == "__main__":
    sensors_processor = sensor_object(INA260_DEVICE_ADDRESSES,
                                      TEMPSENSORS_DEVICE_ADDRESSES)
    csv_handler = CSV_HANDLER(CSV_DIRECTORY, HEADER_LIST)
    csv_handler.csv_write_data_row(HEADER_LIST)
    while 1:
        csv_handler.csv_write_data_cell(datetime.datetime.now())
        sensors_processor.reload_ina_data()

        #write INA current to CSV
        for values in sensors_processor.sensor_data.ina_current_data:
            csv_handler.csv_write_data_cell(values)

        #write INA voltage to CSV
        for values in sensors_processor.sensor_data.ina_voltage_data:
            csv_handler.csv_write_data_cell(values)

        #write ds18b20 temperature to CSV
        sensors_processor.reload_ds_temperature()
        for values in sensors_processor.sensor_data.ds18_temperature_data:
            csv_handler.csv_write_data_cell(values)

        #write onboard raspberry pi temperature to csv
        sensors_processor.reload_raspberry_temperature()
        csv_handler.csv_write_data_cell(
            sensors_processor.sensor_data.raspberry_temperature)
        csv_handler.csv_write_newline()
        print("cycle end")

        time.sleep(1)