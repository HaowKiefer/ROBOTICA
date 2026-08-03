from machine import Pin, time_pulse_us
from utime import sleep_us
from micropython import const

__version__ = '0.2.1'
__author__ = 'Roberto Sánchez'
__license__ = 'Apache License 2.0'

class HCSR04:
    """
    Driver to use the ultrasonic sensor HC-SR04 / JSN-SR04T.
    Sensor range: ~2 cm to ~4 m.
    """

    # echo_timeout_us basado en el rango máximo (~4 m)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: pin de salida (TRIG)
        echo_pin: pin de entrada (ECHO) — usar divisor de voltaje si es 5V
        echo_timeout_us: timeout en microsegundos
        """
        self.echo_timeout_us = echo_timeout_us

        # Pin TRIG
        self.trigger = Pin(trigger_pin, mode=Pin.OUT)
        self.trigger.value(0)

        # Pin ECHO
        self.echo = Pin(echo_pin, mode=Pin.IN)

    def _send_pulse_and_wait(self):
        """
        Envía el pulso TRIG y mide el tiempo del ECHO
        """
        self.trigger.value(0)
        sleep_us(5)
        self.trigger.value(1)
        sleep_us(10)
        self.trigger.value(0)

        pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)

        # time_pulse_us puede devolver valores negativos
        if pulse_time < 0:
            MAX_RANGE_CM = const(500)
            pulse_time = int(MAX_RANGE_CM * 29.1)

        return pulse_time

    def distance_mm(self):
        """
        Devuelve la distancia en milímetros (sin flotantes)
        """
        pulse_time = self._send_pulse_and_wait()
        return pulse_time * 100 // 582

    def distance_cm(self):
        """
        Devuelve la distancia en centímetros (float)
        """
        pulse_time = self._send_pulse_and_wait()
        return (pulse_time / 2) / 29.1

