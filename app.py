"""
@Author:    Prossinger Jakob
@Date:      12 December 2021
@Todo:      * implementation of LED Thread
            * auto reload server data if measuring thread is finished 
"""
from flask import Flask, stream_with_context, request, Response, redirect, url_for
from flask import render_template
from src.sensors import ds18b20
from src.sensors import ina260
from src.sensors import internal
from src.logging.csv_handler import CSVHandler
from src.sensors.sensor_process import SensorObject
import time
import threading
import logging
import RPi.GPIO as GPIO

################## CSV Hanlder Setup #########################
CSV_DIRECTORY = './Logging-Files/sensor_data.csv'
TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]
HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'ds18b28 Temperature', 'raspberry temperature'
]

csv_handler = CSVHandler(CSV_DIRECTORY, HEADER_LIST)
csv_handler.csv_write_data_row(HEADER_LIST)
sensors_processor = SensorObject(INA260_DEVICE_ADDRESSES,
                                 TEMPSENSORS_DEVICE_ADDRESSES, csv_handler)

################## Logger Setup ##############################
logger = logging.getLogger("strato_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)-12s - %(levelname)s:\n\tat %(funcName)s() - %(message)s'
)
console_Handler = logging.StreamHandler()
console_Handler.setLevel(logging.INFO)
console_Handler.setFormatter(formatter)
file_Hanlder = logging.FileHandler('./Logging-Files/sensor_data.csv')
file_Hanlder.setLevel(logging.ERROR)
file_Hanlder.setFormatter(formatter)
logger.addHandler(console_Handler)
logger.addHandler(file_Hanlder)

################ Falsk App Setup #############################
app = Flask(__name__)
app.run_main_system = False
app.LED_activated = True


def system_main_thread() -> None:
    if app.run_main_system is False:
        return
    sensors_processor.system_process()
    logger.info("started system main thread")
    threading.Timer(5, system_main_thread).start()


def led_blink_thread() -> None:
    if app.LED_activated is False:
        GPIO.cleanup()
        return
    else:
        pass


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


@app.route('/stream')
def stream_view():
    raspberry_temp = internal.get_raspberry_temperature()
    return Response(
        stream_template('template.html', raspberry_temp=raspberry_temp))


@app.route("/")
def main():
    template_data = {'main_process': app.run_main_system}
    return render_template('index.html', **template_data)


@app.route("/changeProcess/<aMode>")
def change_system_main_thread(aMode):
    if aMode == "on":
        app.run_main_system = True
        system_main_thread()
    elif aMode == "off":
        app.run_main_system = False

    return redirect("/")


@app.route("/sensors")
def show_values():
    sensors_processor.system_process()
    template_data = {
        'ina260_voltages': sensors_processor.sensor_data.ina_voltage_data,
        'ina260_currents': sensors_processor.sensor_data.ina_current_data,
        'raspbi_temp': sensors_processor.sensor_data.raspberry_temperature,
        'ds18b20_temp': sensors_processor.sensor_data.ds18_temperature_data
    }
    raspberry_temp = internal.get_raspberry_temperature()
    return render_template('template.html', **template_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
