from sensor.ina260 import INA260
import time


def main() -> None:
    device_address = 0x40
    ina260_sensor = INA260("Ina260_sensor", address=device_address)

    while 1:
        voltage = ina260_sensor.get_bus_voltage()
        voltage_average = ina260_sensor.get_voltage_average()
        current = ina260_sensor.get_current()
        print(
            f'Spannung: {voltage}\nMittelwert Spannung: {voltage_average}\nStrom: {current}')
        time.sleep(5)


if __name__ == '__main__':
    main()
