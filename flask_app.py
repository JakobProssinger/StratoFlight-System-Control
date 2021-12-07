from flask import Flask, stream_with_context, request, Response, flash
from flask import render_template
from src.sensors import internal

import time

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