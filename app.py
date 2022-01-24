#!/usr/bin/env python3
"""
@File:          app.py
@Descrption:    Systemcontroll of Stratoflight
@Author:        Prossinger Jakob
@Date:          23 January 2022
@Todo:          * add LED BLink 
                * add logging TODO
                * add sensor reading thread 
"""
from pathlib import Path
from sensor import ina260
from sensor import sensor
from sensor import neo6m
from sensor import internal

from flask import Flask, request, redirect, render_template
from csv_handler.csv_handler import CSV_HANDLER


app = Flask(__name__)


@app.route("/")
def main() -> None:
    template_data = {
    }
    return render_template('index.html', **template_data)


@app.route("/sensors")
def show_data() -> None:
    strato_controller.reload()
    template_data = {
        'sensors': strato_controller.sensors
    }
    return render_template('sensor_data.html', **template_data)


if __name__ == "__main__":
    sensor_ina1 = ina260.INA260("INA260 Primary", 0x40)
    sensor_ina2 = ina260.INA260("INA260 Secondary", 0x41)
    sensor_neo = neo6m.NEO6M(name="NEO6M GPS")
    sensor_internal = internal.INTERNAL("Raspberry")

    strato_csv_handler = CSV_HANDLER("data/sensor_data.csv")
    strato_controller = sensor.Controller(
        "strato_controller", strato_csv_handler)
    strato_controller.addSensor(sensor_internal)
    strato_controller.addSensor(sensor_ina1)
    strato_controller.addSensor(sensor_ina2)
    strato_controller.addSensor(sensor_neo)
    strato_controller.write_csv_header()
    app.run(host="0.0.0.0", port=5000, debug=False)
