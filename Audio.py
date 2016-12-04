import pyaudio
import wave
import threading
import logging
log = logging.getLogger("Audio")

p = pyaudio.PyAudio()
CHUNK = 1024


class AudioControl:
    def __init__(self):
        self.play_thread = AudioThread("")
        self._stream = None
        self._recFile = None

    def stop_sound(self):
        self.play_thread.stop = True  # stop the audio playing

    def play_sound(self, filename):
        self.play_thread = AudioThread(filename)
        self.play_thread.start()

    def start_recording(self, filename):
        log.info("Start recording")
        self.stop_sound()

        rate = 22050
        self._recFile = wave.open(filename, 'wb')
        self._recFile.setnchannels(1)
        self._recFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        self._recFile.setframerate(rate)

        self._stream = p.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=rate,
                              input=True,
                              frames_per_buffer=CHUNK,
                              stream_callback=self.get_callback())
        self._stream.start_stream()

    def stop_recording(self):
        self._stream.stop_stream()
        self._stream.close()
        self._recFile.close()
        log.info("Recording done!")

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self._recFile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


class AudioThread (threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename
        self.stop = False

    def run(self):
        log.debug("Starting audio thread: " + self.filename)
        wf = wave.open(self.filename + ".wav", 'rb')

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != '' and self.stop is False:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        log.debug("Exiting audio thread: " + self.filename)

control = AudioControl()