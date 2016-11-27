
# import RPi.GPIO as GPIO
import GPIO_dummy as GPIO  # dummy GPIO for development off board
import Playlist
import Audio
import time
import Config
import Votes
import ServerCommunication
import atexit
from threading import Timer
import threading


PLAY_PIN        = 11
RECORD_PIN      = 11
VOTE_UP_PIN     = 11
VOTE_DOWN_PIN   = 11

NUMBER_OF_LEDS  = 16


class State:
    NONE            = 0
    CITY_VOICE      = 1
    USER_VOICE      = 2
    RECORDING       = 3
    value = NONE

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

        for i in range(0, NUMBER_OF_LEDS-1):
            print "LED: " + str(i)  # TODO: add actual led driving code here!
            time.sleep(float(Config.recording_time)/NUMBER_OF_LEDS)

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


def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PLAY_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RECORD_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(VOTE_UP_PIN,     GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(VOTE_DOWN_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(PLAY_PIN,         GPIO.FALLING, callback=play_callback,       bouncetime=200)
    GPIO.add_event_detect(RECORD_PIN,       GPIO.FALLING, callback=record_callback,     bouncetime=200)
    GPIO.add_event_detect(VOTE_UP_PIN,      GPIO.FALLING, callback=vote_up_callback,    bouncetime=200)
    GPIO.add_event_detect(VOTE_DOWN_PIN,    GPIO.FALLING, callback=vote_down_callback,  bouncetime=200)

    state.value = State.CITY_VOICE


def cleanup():
    GPIO.cleanup()

atexit.register(cleanup)
