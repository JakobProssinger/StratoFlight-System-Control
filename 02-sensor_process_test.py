from src.sensors.sensor_process import sensor_object
import time

TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]

if __name__ == "__main__":
    data = sensor_object(INA260_DEVICE_ADDRESSES, TEMPSENSORS_DEVICE_ADDRESSES)
    while 1:
        data.reload_ina_data()
        print("Voltage mV:\t", data.ina_voltage)
        print("Current mA:\t", data.ina_current)
        data.reload_ds_temperature()
        print("Temp ds18 °C:\t", data.ds18b20_temperature_list)
        time.sleep(1)
