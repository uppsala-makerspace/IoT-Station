import alsaaudio
import wave
import logging
import threading
log = logging.getLogger("Audio")

CHUNK = 1024


class AudioControl:
    def __init__(self):
        self.audio_thread = AudioThread("")
        self._stream = None
        self._wf = None

    def stop_sound(self):
        self.audio_thread.stop = True
        log.info("Playing done!")

    def play_sound(self, filename):
        log.info("Start playing: " + filename)

        self.audio_thread = AudioThread(filename)
        self.audio_thread.start()

    def start_recording(self, filename):
        log.info("Start recording")
        self.stop_sound()
        self.audio_thread = AudioThread(filename, False)
        self.audio_thread.start()

    def stop_recording(self):
        self.stop_sound()
        log.info("Recording done!")


class AudioThread (threading.Thread):
    def __init__(self, filename, play=True):
        threading.Thread.__init__(self)
        self.filename = filename
        self.stop = False
        self.play = play

    def run(self):
        log.debug("Starting audio thread: " + self.filename)

        if self.play is True:
            wf = wave.open(self.filename + ".wav", 'rb')

            # Set attributes
            device = alsaaudio.PCM()
            device.setchannels(wf.getnchannels())
            device.setrate(wf.getframerate())

            # 8bit is unsigned in wav files
            if wf.getsampwidth() == 1:
                device.setformat(alsaaudio.PCM_FORMAT_U8)
            # Otherwise we assume signed data, little endian
            elif wf.getsampwidth() == 2:
                device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            elif wf.getsampwidth() == 3:
                device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
            elif wf.getsampwidth() == 4:
                device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
            else:
                raise ValueError('Unsupported format')

            device.setperiodsize(CHUNK)

            data = wf.readframes(CHUNK)
            while data != '' and self.stop is False:
                device.write(data)
                data = wf.readframes(CHUNK)

        else:
            # record
            rate = 22050

            wf = wave.open(self.filename + ".wav", 'wb')

            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)

            device = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)

            device.setchannels(1)
            device.setrate(rate)
            device.setformat(alsaaudio.PCM_FORMAT_S16_LE)

            device.setperiodsize(CHUNK)

            while self.stop is False:
                l, data = device.read()
                if l:
                    wf.writeframes(data)

        wf.close()
        device.close()
        log.debug("Exiting audio thread: " + self.filename)


control = AudioControl()
