from flask import Flask, stream_with_context, request, Response, flash
from flask import render_template
from src.sensors import ds18b20
from src.sensors import ina260
from src.sensors import internal
from src.logging.csv_handler import CSVHandler
from src.sensors.sensor_process import SensorObject
import time

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

app = Flask(__name__)


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

    return render_template('index.html')


@app.route("/value")
def show_values():
    raspberry_temp = internal.get_raspberry_temperature()
    return render_template('template.html', raspberry_temp=raspberry_temp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)