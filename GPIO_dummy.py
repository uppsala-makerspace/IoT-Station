import logging
log = logging.getLogger("GPIO_dummy")

LOW = 0
HIGH = 1
OUT = 2
IN = 3
PUD_OFF = 4
PUD_DOWN = 5
PUD_UP = 6
BCM = 7
RISING = 8
FALLING = 9


def setmode(mode):
    log.debug("set mode: " + str(mode))


def setup(channel, state, initial=-1, pull_up_down=-1):
    log.debug("setup: " + str(channel) + " " + str(state))


def add_event_detect(channel, edge, callback, bouncetime):
    log.debug("add event detect: " + str(channel) + " " + str(edge))


def output(pin, value):
    log.debug("output: " + str(pin) + " = " + str(value))


def cleanup():
    log.info("cleanup")

