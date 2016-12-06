import pyaudio
import wave
import logging
log = logging.getLogger("Audio")

p = pyaudio.PyAudio()
CHUNK = 1024


class AudioControl:
    def __init__(self):
        self._stream = None
        self._wf = None

    def stop_sound(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        self._wf.close()
        log.info("Playing done!")

    def play_sound(self, filename):
        log.info("Start playing: " + filename)

        if self._stream is not None and self._stream.is_active():
            self.stop_sound()

        self._wf = wave.open(filename + ".wav", 'rb')

        self._stream = p.open(format=p.get_format_from_width(self._wf.getsampwidth()),
                              channels=self._wf.getnchannels(),
                              rate=self._wf.getframerate(),
                              output=True,
                              stream_callback=self.get_callback_play())
        # self._stream.start_stream()

    def get_callback_play(self):
        def callback(in_data, frame_count, time_info, status):
            data = self._wf.readframes(frame_count)
            return data, pyaudio.paContinue
        return callback

    def start_recording(self, filename):
        log.info("Start recording")
        self.stop_sound()

        rate = 22050
        self._wf = wave.open(filename, 'wb')
        self._wf.setnchannels(1)
        self._wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        self._wf.setframerate(rate)

        self._stream = p.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=rate,
                              input=True,
                              frames_per_buffer=CHUNK,
                              stream_callback=self.get_callback_record())
        # self._stream.start_stream()

    def stop_recording(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        self._wf.close()
        log.info("Recording done!")

    def get_callback_record(self):
        def callback(in_data, frame_count, time_info, status):
            self._wf.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


control = AudioControl()