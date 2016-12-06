try:
    import RPi.GPIO as GPIO
except ImportError:
    import GPIO_dummy as GPIO


RCLK_PIN = 25
SRCLK_PIN = 24
SERIAL_PIN = 23


class BitShifter:
    def __init__(self, number_of_bits=8):
        self.numberOfBits = number_of_bits
        self.bits = list()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RCLK_PIN, GPIO.OUT)
        GPIO.setup(SRCLK_PIN, GPIO.OUT)
        GPIO.setup(SERIAL_PIN, GPIO.OUT)
        self.set_all(GPIO.LOW)

    def set_all(self, mode, now=True):
        for i in range(0, self.numberOfBits):
            self.bits.insert(i, mode)
        if now is True:
            self.transmit()

    def set(self, bit, mode, now=True):
        self.bits[bit] = mode
        if now is True:
            self.transmit()

    def transmit(self):
        GPIO.output(RCLK_PIN, GPIO.LOW)

        for bit in range(self.numberOfBits-1, -1, -1):
            GPIO.output(SRCLK_PIN, GPIO.LOW)
            GPIO.output(SERIAL_PIN, self.bits[bit])
            GPIO.output(SRCLK_PIN, GPIO.HIGH)

        GPIO.output(RCLK_PIN, GPIO.HIGH)
