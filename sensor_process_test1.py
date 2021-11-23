from src.sensors.sensor_process import sensor_data_object
import time

TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]

if __name__ == "__main__":
    data = sensor_data_object(INA260_DEVICE_ADDRESSES,
                              TEMPSENSORS_DEVICE_ADDRESSES)
    while 1:
        data.reload_ina_data()
        print("Voltage mV: ", [1000 * i for i in data.ina_voltage])
        print("Current mA: ", [1000 * i for i in data.ina_current])
        data.reload_ds_temperature()
        print("Temp ds18 °C: ", data.ds18b20_values)
        time.sleep(1)
