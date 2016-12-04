try:
    import RPi.GPIO as GPIO
except ImportError:
    import GPIO_dummy as GPIO

from BitShifter import BitShifter
from threading import Timer

NUMBER_OF_LEDS = 8
array = BitShifter()


class CountDown:
    def __init__(self):
        self.cnt = NUMBER_OF_LEDS-1
        array.set_all(GPIO.HIGH)

    def tick(self):
        self.cnt -= 1
        array.set(self.cnt, GPIO.LOW)


class BlinkAll:
    def __init__(self, times, interval):
        self.times = times
        self.on = True
        self.interval = interval
        self.cancelled = False
        array.set_all(GPIO.HIGH)
        self.t = Timer(self.interval, self.tick)

    def tick(self):
        if self.cancelled is True:
            return

        if self.on:
            self.times -= 1
            if self.times == 0:
                return

            array.set_all(GPIO.LOW)
            self.on = False
        else:
            array.set_all(GPIO.HIGH)
            self.on = True

        t = Timer(self.interval, self.tick)
        t.start()

    def cancel(self):
        self.cancelled = True

