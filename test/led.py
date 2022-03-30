import threading
import RPi.GPIO as GPIO

# initialisierung der globalen Variablen
_LED_PIN_RED = 11
_LED_PIN_GREEN = 13

global LED_states
LED_states = {

    _LED_PIN_RED: {
        'state': GPIO.HIGH
    },
    _LED_PIN_GREEN: {
        'state': GPIO.LOW
    }
}


def gpio_setup() -> None:
    # initialisierung GPIO Pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for pin in LED_states:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, LED_states[pin]['state'])


def led_blink_thread() -> None:
    for pin in app.LED_states:
        # invertieren des aktuellen LED Zustands
        app.LED_states[pin]['state'] = not app.LED_states[pin]['state']
        GPIO.output(pin, app.LED_states[pin]['state'])
    # selbst Aufruf in 1,5 Sekunden
    threading.Timer(1.5, led_blink_thread).start()


def main() -> None:
    while 1:
        pass


if __name__ == "__main__":
    gpio_setup()
    # Thread Starten
    led_blink_thread()
    # Start des Hauptprogramms
    main()
