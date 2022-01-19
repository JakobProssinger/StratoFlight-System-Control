"""
@File:          app.py
@Descrption:    starts flask server for Strato Flight 2021/2022
@Author:        Prossinger Jakob
@Date:          19 January 2021
@Todo:          * auto reload server data if measuring thread is finished
                * setup function: logging, sensor data, csv file existing
                * comments Parameters and functions
                * error if /Logging-Files does not exist
                * only write header if file is empty
                * shutdown under 2,7V
                * Polymorph all Sensors
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
import constants as const
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
INA260_DEVICE_ADDRESSES = const._INA260_DEVICE_ADDRESSES
HEADER_LIST = const._CSV_HEADER_LIST

csv_handler = CSVHandler(CSV_DATA_DIRECTORY, HEADER_LIST)
csv_handler.csv_write_data_row(HEADER_LIST)
sensors_processor = SensorObject(INA260_DEVICE_ADDRESSES, csv_handler)

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

app.led_blink_state = const._AUTOSTART_LED_BLINK
app.run_main_system = const._AUTOSTART_MEASURING

default_LED_states = {

    const._LEDPIN1: {
        'name': "Red_LED_PIN",
        'state': GPIO.HIGH
    },
    const._LEDPIN2: {
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
    if app.led_blink_state is False:
        return
    for pin in app.LED_states:
        app.LED_states[pin]['state'] = not app.LED_states[pin]['state']
        GPIO.output(pin, app.LED_states[pin]['state'])
    logger.info("started led blink thread")
    threading.Timer(1, led_blink_thread).start()


# start led blink if 'flask run' is used
if app.led_blink_state == True:
    led_blink_thread()


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
        'led_blink_mode': app.led_blink_state
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
        app.led_blink_state = True
        led_blink_thread()
    elif aMode == "off":
        app.led_blink_state = False

    return redirect("/")


@app.route("/sensors")
def show_values():
    sensors_processor.system_process()
    template_data = {
        'ina260_voltages': sensors_processor.sensor_data.ina_voltage_data,
        'ina260_currents': sensors_processor.sensor_data.ina_current_data,
        'raspbi_temp': sensors_processor.sensor_data.raspberry_temperature,
    }
    return render_template('template.html', **template_data)


if __name__ == '__main__':
    led_blink_thread()
    app.run(host=const._IP_PRIMARY, port=5000, debug=True)
