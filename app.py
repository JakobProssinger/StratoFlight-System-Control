#!/usr/bin/env python3
"""
@File:          app.py
@Descrption:    Systemcontroll of Stratoflight
@Author:        Prossinger Jakob
@Date:          9 March 2022
@Todo:          * add logging TODO
"""
from sensor import ina260
from sensor import sensor
from sensor import neo6m
from sensor import internal
from sensor import dht22
from controller import controller
from controller.secondary import secondary
from config import *
import config as config
from flask import Flask, redirect, render_template, send_file
from csv_handler.csv_handler import CSV_HANDLER
import RPi.GPIO as GPIO
import atexit
import threading


app = Flask(__name__)
app.LED_states = default_LED_states

# init GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
for pin in app.LED_states:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, app.LED_states[pin]['state'])

for pin in config._REQUEST_SHUTDOWN_PINS:
    GPIO.setup(pin, GPIO.OUT)

for pin in config._POWER_OFF_PINS:
    GPIO.setup(pin, GPIO.OUT)


@atexit.register
def atexit_function() -> None:
    GPIO.cleanup()


def led_blink_thread() -> None:
    for pin in app.LED_states:
        app.LED_states[pin]['state'] = not app.LED_states[pin]['state']
        GPIO.output(pin, app.LED_states[pin]['state'])
    threading.Timer(config._BLINK_INTERVAL_SEC, led_blink_thread).start()


def sensor_reading_thread() -> None:
    strato_controller.reload()
    strato_controller.write_csv_data()
    ina260_secondary_voltage = ina260_secondary.get_voltage_average()
    check_shutdown(strato_controller, ina260_secondary_voltage)
    check_turn_on(strato_controller, ina260_secondary_voltage)
    threading.Timer(config._MEASURING_INTERVAL_SEC,
                    sensor_reading_thread).start()


def check_shutdown(a_controller: controller, ina_voltage: float) -> None:
    if type(ina_voltage) != float:
        return
    for raspberry in a_controller.secondaries.values():
        # continue to next raspberry if raspberry is already shutdowned
        if raspberry.get_Power_status() == secondary.Secondary.SHUTDOWN:
            continue
        if raspberry.get_Shutdown_voltage() > ina_voltage:
            # request shutdown if shutdown has not been requested
            if raspberry.get_Request_status() == secondary.Secondary.NOT_SHUTDOWN_REQUEST:
                raspberry.request_shutdown()
                print(f'request shutdown secondary : {raspberry.get_Name()}')
            # shutdown raspberry
            else:
                raspberry.shutdown()
                print(f'shutdown secondary : {raspberry.get_Name()}')


def check_turn_on(a_controller: controller, ina_voltage: float) -> None:
    if type(ina_voltage) != float:
        return
    for raspberry in a_controller.get_Scondaries().values():
        if raspberry.get_Power_status() == secondary.Secondary.SHUTDOWN:
            if raspberry.get_Power_on_voltage() <= ina_voltage:
                raspberry.turn_on()
                print(f'turned on secondary : {raspberry.get_Name()}')


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/sensors")
def show_data():
    # read new data from all sensors
    strato_controller.reload()
    # store data in csv file
    strato_controller.write_csv_data()
    template_data = {
        'sensors': strato_controller.sensors
    }
    return render_template('sensor_data.html', **template_data)


@app.route("/status")
def show_status():
    template_data = {
        'secondary_voltage': ina260_secondary.get_voltage_average(),
        'raspberries': strato_controller.get_Scondaries(),
        'SHUTDOWN_REQUEST': secondary.Secondary.SHUTDOWN_REQUEST,
        'SHUTDOWN': secondary.Secondary.SHUTDOWN,
    }
    return render_template('status_window.html', **template_data)


@app.route("/getCSV")  # this is a job for GET, not POST
def plot_csv():
    return send_file('/home/pi/Documents/StratoFlight-System-Control/data/sensor_data.csv',
                     mimetype='text/csv',
                     attachment_filename='sensor_data.csv',
                     as_attachment=True)


if __name__ == "__main__":
    # init csv handler
    strato_csv_handler = CSV_HANDLER(
        "/home/pi/Documents/StratoFlight-System-Control/data/sensor_data.csv")

    # init controller
    strato_controller = controller.Controller(
        "strato_controller", strato_csv_handler)

    # init all sensors
    ina260_secondary = ina260.INA260(
        "INA260 Secondary I", config._SECONDARY1_INA260_ADDRESS)
    ina260_primary = ina260.INA260(
        "INA260 Primary", config._PRIMARY_INA260_ADDRESS)
    sensor_neo = neo6m.NEO6M(name="NEO6M GPS")
    sensor_internal = internal.INTERNAL("Raspberry")
    sensor_dht22 = dht22.DHT22("Temperature_Humidity", config._DHT22_PIN)

    # add sensors to controller
    strato_controller.addSensor(sensor_internal)
    strato_controller.addSensor(ina260_secondary)
    strato_controller.addSensor(ina260_primary)
    strato_controller.addSensor(sensor_neo)
    strato_controller.addSensor(sensor_dht22)

    # init secondaries
    secondary1 = secondary.Secondary(
        "secondary1", config._SECONDARY1_REQUEST_SHUTDOWN_PIN,
        config._SECONDARY1_POWER_OFF_PIN,
        config._SECONDARY1_SHUTDOWN_VOLTAGE,
        config._SECONDARY1_POWER_ON_VOLTAGE)

    secondary2 = secondary.Secondary(
        "secondary2", config._SECONDARY2_REQUEST_SHUTDOWN_PIN,
        config._SECONDARY2_POWER_OFF_PIN,
        config._SECONDARY2_SHUTDOWN_VOLTAGE,
        config._SECONDARY2_POWER_ON_VOLTAGE)
    secondary3 = secondary.Secondary(
        "secondary3", config._SECONDARY3_REQUEST_SHUTDOWN_PIN,
        config._SECONDARY3_POWER_OFF_PIN,
        config._SECONDARY3_SHUTDOWN_VOLTAGE,
        config._SECONDARY3_POWER_ON_VOLTAGE)
    secondary4 = secondary.Secondary(
        "secondary4", config._SECONDARY4_REQUEST_SHUTDOWN_PIN,
        config._SECONDARY4_POWER_OFF_PIN,
        config._SECONDARY4_SHUTDOWN_VOLTAGE,
        config._SECONDARY4_POWER_ON_VOLTAGE)

    # add secondaries to controller
    strato_controller.add_Secondary(secondary1)
    strato_controller.add_Secondary(secondary2)
    strato_controller.add_Secondary(secondary3)
    strato_controller.add_Secondary(secondary4)
    strato_controller.write_csv_header()
    # starting led blink thread
    led_blink_thread()
    # start sensor reading thread
    sensor_reading_thread()
    app.run(port=5000)
