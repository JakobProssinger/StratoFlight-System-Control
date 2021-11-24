from src.sensors.sensor_process import sensor_object
import time

TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]

if __name__ == "__main__":
    sensors_processor = sensor_object(INA260_DEVICE_ADDRESSES,
                                      TEMPSENSORS_DEVICE_ADDRESSES)
    while 1:
        sensors_processor.reload_ina_data()
        print("Voltage mV:\t", sensors_processor.sensor_data.ina_voltage_data)
        print("Current mA:\t", sensors_processor.sensor_data.ina_current_data)
        sensors_processor.reload_ds_temperature()
        print("Temp ds18 °C:\t",
              sensors_processor.sensor_data.ds18_temperature_data)
        time.sleep(1)
