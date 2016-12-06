
try:
    import RPi.GPIO as GPIO
except ImportError:
    import GPIO_dummy as GPIO  # dummy GPIO for development off board

import Playlist
import Audio
import time
import Config
import Votes
import ServerCommunication
import atexit
import threading
import LED


PLAY_PIN = 11
RECORD_PIN = 12
VOTE_UP_PIN = 15
VOTE_DOWN_PIN = 14


class State:
    NONE = 0
    CITY_VOICE = 1
    USER_VOICE = 2
    RECORDING = 3

    def __init__(self):
        self.value = State.NONE

state = State()


def play_callback():
    # TODO: not properly implemented yet
    if state.value is State.RECORDING:
        return

    state.value = State.USER_VOICE
    time.sleep(10)
    state.value = State.CITY_VOICE


class RecordThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False

    def run(self):
        state.value = State.RECORDING
        Playlist.control.stop()

        Audio.control.start_recording(Config.data_path + "/rec.wav")

        leds = LED.CountDown()
        for i in range(0, LED.NUMBER_OF_LEDS-1):
            leds.tick()
            time.sleep(float(Config.recording_time)/LED.NUMBER_OF_LEDS)

        Audio.control.stop_recording()
        ServerCommunication.post_audio_message(Config.data_path + "/rec")

        state.value = State.CITY_VOICE

        # TODO: we should sleep longer here...
        time.sleep(2.0)
        Playlist.control.play()


def record_callback():
    record_thread = RecordThread()
    record_thread.start()


def vote_up_callback():
    if state.value is not State.USER_VOICE:
        return

#   TODO: need proper id of playing audio here
    Votes.add_vote("922ae72c-1862-4d91-a08b-4f2738ad0354", True)


def vote_down_callback():
    if state.value is not State.USER_VOICE:
        return

#   TODO: need proper id of playing audio here
    Votes.add_vote("922ae72c-1862-4d91-a08b-4f2738ad0354", False)


def button_callback(pin):
    if pin is PLAY_PIN:
        play_callback()
    elif pin is RECORD_PIN:
        record_callback()
    elif pin is VOTE_DOWN_PIN:
        vote_down_callback()
    elif pin is VOTE_UP_PIN:
        vote_up_callback()


def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PLAY_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RECORD_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(VOTE_UP_PIN,     GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(VOTE_DOWN_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(PLAY_PIN,         GPIO.RISING, callback=button_callback,  bouncetime=200)
    GPIO.add_event_detect(RECORD_PIN,       GPIO.RISING, callback=button_callback,  bouncetime=200)
    GPIO.add_event_detect(VOTE_UP_PIN,      GPIO.RISING, callback=button_callback,  bouncetime=200)
    GPIO.add_event_detect(VOTE_DOWN_PIN,    GPIO.RISING, callback=button_callback,  bouncetime=200)

    state.value = State.CITY_VOICE


def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)
