"""
@File:          app.py
@Descrption:    starts flask server for Strato Flight 2021/2021
@Author:        Prossinger Jakob
@Date:          14 December 2021
@Todo:          * auto reload server data if measuring thread is finished
                * setup function: logging, sensor data, csv file existing
                * LOGGING LEVEL: SYSTEM
                * comments Parameters and functions
                * KONSTANTEN in externes File z.B. LED Pins
                * error if /Logging-Files does not exist
"""
from flask import Flask, stream_with_context, request, Response, redirect, url_for
from flask import render_template
from src.sensors import internal
from src.logging.csv_handler import CSVHandler
from src.sensors.sensor_process import SensorObject
import threading
import logging
import RPi.GPIO as GPIO
import atexit
"""
    Script to start the flask server and handle all sensor in
    the Project: StratoFlight 2021/2022. 

    Attributes
    ----------
    CSV_DATA_DIRECTORY : str
        PATH to the csv file to store all sensor data.

    TEMPSENSORS_DEVICE_ADDRESSES : list (int)
        List of addresses of the DS18b20 sensor for temperature measurement.

    INA260_DEVICE_ADDRESSES : list (int)
        List of addresses of the INA260 sensor for electrical current and
        voltage measurement.

    HEADER_LIST : list (string)
        List of csv file headeres for the csv file data file.

    csv_handler :  CSVHandler
        csv handler, stores the data in the csv data file.

    sensors_processor : SensorObject
        object to handle all sensor measurements and storing them
        inside varibale.
    
    logger : logger
        StratoFlight main/parent logger to handle all loggings inside
        this project

    formatter : logging.Formatter
        formatter for the logging system

    console_Handler : logging.StreamHandler


    file_Hanlder
    


    Methods
    -------
    csv_write_header(self)
        write the header column to the csv file
    
"""
################## CSV Hanlder Setup #########################
CSV_DATA_DIRECTORY = '/home/pi/Documents/StratoFlight-System-Control/Logging-Files/sensor_data.csv'
TEMPSENSORS_DEVICE_ADDRESSES = ['28-00000cdfc36f']  #, '28-00000cdf6b81']
INA260_DEVICE_ADDRESSES = [0x40, 0x41]
HEADER_LIST = [
    'TIME', 'INA CURRENT 1/mA', 'INA CURRENT 2/mA', 'INA VOLTAGE 1/mV',
    'INA VOLTAGE 2/mV', 'ds18b28 Temperature', 'raspberry temperature'
]

csv_handler = CSVHandler(CSV_DATA_DIRECTORY, HEADER_LIST)
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
file_Hanlder = logging.FileHandler(
    '/home/pi/Documents/StratoFlight-System-Control/Logging-Files/logging_error.csv'
)
file_Hanlder.setLevel(logging.ERROR)
file_Hanlder.setFormatter(formatter)
logger.addHandler(console_Handler)
logger.addHandler(file_Hanlder)

################ flask app setup #############################
app = Flask(__name__)
app.run_main_system = False
app.LED_blink_state = False

default_LED_states = {
    11: {
        'name': "Red_LED_PIN",
        'state': GPIO.HIGH
    },
    13: {
        'name': "Green_LED_PIN",
        'state': GPIO.LOW
    }
}

app.LED_states = default_LED_states
GPIO.setmode(GPIO.BOARD)
for pin in app.LED_states:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, app.LED_states[pin]['state'])


@atexit.register
def atexit_function() -> None:
    GPIO.cleanup()


################ flask app functions #############################
def system_main_thread() -> None:
    if app.run_main_system is False:
        return
    sensors_processor.system_process()
    logger.info("started system main thread")
    threading.Timer(5, system_main_thread).start()


def led_blink_thread() -> None:
    if app.LED_blink_state is False:
        return
    for pin in app.LED_states:
        app.LED_states[pin]['state'] = not app.LED_states[pin]['state']
        GPIO.output(pin, app.LED_states[pin]['state'])
    logger.info("started led blink thread")
    threading.Timer(1, led_blink_thread).start()


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


################ flask app routes #############################
@app.route('/stream')
def stream_view():
    raspberry_temp = internal.get_raspberry_temperature()
    return Response(
        stream_template('template.html', raspberry_temp=raspberry_temp))


@app.route("/")
def main():
    template_data = {
        'main_process': app.run_main_system,
        'led_blink_mode': app.LED_blink_state
    }
    return render_template('index.html', **template_data)


@app.route("/changeProcess/<aMode>")
def change_system_main_thread(aMode):
    if aMode == "on":
        app.run_main_system = True
        system_main_thread()
    elif aMode == "off":
        app.run_main_system = False

    return redirect("/")


@app.route("/changeBlinkMode/<aMode>")
def change_Blink_Mode(aMode):
    if aMode == "on":
        app.LED_blink_state = True
        led_blink_thread()
    elif aMode == "off":
        app.LED_blink_state = False

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
    return render_template('template.html', **template_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
