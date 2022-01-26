#!/usr/bin/env python3
"""
@File:          app.py
@Descrption:    Systemcontroll of Stratoflight
@Author:        Prossinger Jakob
@Date:          24 January 2022
@Todo:          * add logging TODO
                * find better way to init flask app with settings TODO 
"""
from sensor import ina260
from sensor import sensor
from sensor import neo6m
from sensor import internal
from config import *
from flask import Flask, redirect, render_template
from csv_handler.csv_handler import CSV_HANDLER
import RPi.GPIO as GPIO
import atexit
import threading


app = Flask(__name__)
app.led_blink_state = True
app.run_main_system = True
app.LED_states = default_LED_states
GPIO.setmode(GPIO.BOARD)
for pin in app.LED_states:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, app.LED_states[pin]['state'])


@atexit.register
def atexit_function() -> None:
    print("exited")
    GPIO.cleanup()


def led_blink_thread() -> None:
    global app
    if app.led_blink_state is False:
        return
    for pin in app.LED_states:
        app.LED_states[pin]['state'] = not app.LED_states[pin]['state']
        GPIO.output(pin, app.LED_states[pin]['state'])
    threading.Timer(1.5, led_blink_thread).start()


def sensor_reading_thread() -> None:
    if app.run_main_system is False:
        return
    strato_controller.reload()
    strato_controller.write_csv_data()
    threading.Timer(25, sensor_reading_thread).start()


@app.route("/")
def main() -> None:
    template_data = {
        'led_blink_mode': app.led_blink_state
    }
    return render_template('index.html', **template_data)


@app.route("/sensors")
def show_data() -> None:
    strato_controller.reload()
    strato_controller.write_csv_data()
    template_data = {
        'sensors': strato_controller.sensors
    }
    return render_template('sensor_data.html', **template_data)


@app.route("/changeBlinkMode/<aMode>")
def change_Blink_Mode(aMode):
    if aMode == "on":
        app.led_blink_state = True
        led_blink_thread()
    elif aMode == "off":
        app.led_blink_state = False

    return redirect("/")


if __name__ == "__main__":
    sensor_ina1 = ina260.INA260("INA260 Primary", 0x40)
    sensor_ina2 = ina260.INA260("INA260 Secondary", 0x41)
    sensor_neo = neo6m.NEO6M(name="NEO6M GPS")
    sensor_internal = internal.INTERNAL("Raspberry")

    strato_csv_handler = CSV_HANDLER("/home/pi/Documents/StratoFlight-System-Control-main/data/sensor_data.csv")
    strato_controller = sensor.Controller(
        "strato_controller", strato_csv_handler)
    strato_controller.addSensor(sensor_internal)
    strato_controller.addSensor(sensor_ina1)
    strato_controller.addSensor(sensor_ina2)
    strato_controller.addSensor(sensor_neo)
    strato_controller.write_csv_header()

    led_blink_thread()
    sensor_reading_thread()
    app.run(host="0.0.0.0", port=5000, debug=True)
