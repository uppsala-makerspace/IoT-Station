import base64
import os
from threading import Timer
import Config
import ServerCommunication
import Audio
import Speex

import logging
log = logging.getLogger("Playlist")

MIN_MESSAGES_IN_PLAYLIST = 2


class VoiceMessage:
    messageId = ""
    length = 0

    def __init__(self, message_id, length):
        self.messageId = message_id
        self.length = length


class PlaybackControls:
    def __init__(self):
        self.currentPlayingMessage = 0
        self.t = None
        self.timerStarted = 0
        self.pauseTimer = 0
        self.playlist = []
        self.emergency_playlist = []

    def play(self):
        """Play the current message"""
        if len(self.playlist) is 0:
            log.error("Playlist is empty!")
            return

        m = self.playlist[0]

        # TODO: add proper audio length
        self.t = Timer(3.0 + Config.sensor_message_delay, self.play_next)
        self.t.start()

        Audio.control.play_sound(get_filename(m.messageId))
        log.info("Playing " + m.messageId + " (" + str(m.length) + "s)")

    def play_next(self):
        """Play the next message"""
        remove_first_voice_message()
        self.play()

    def stop(self):
        """Cancel playing the current sound"""
        if self.t is not None:
            self.t.cancel()
        remove_first_voice_message()

    def pause(self):
        """Not implemented"""

control = PlaybackControls()


def get_filename(message_id):
    return Config.data_path + "/voice-" + message_id


def add_voice_message(m):
    """Add a voice message to the list and save it to disk"""
    message = VoiceMessage(m['message']['uuid'], m['offset'])
    control.playlist.append(message)

    filename = get_filename(m['message']['uuid'])
    log.info("Message added to playlist: " + filename)

    # if the file already exists (rara, but could happen if we get the same message from the server), bail out
    if os.path.isfile(filename + ".wav"):
        return

    if m['message']['mimeType'] == "audio/x-speex":
        extension = ".spx"
    else:
        extension = ".wav"

    # write data to disk
    spx_data = base64.b64decode(m['message']['base64Data'])
    with open(filename + extension, 'wb') as f:
        f.write(spx_data)

    if m['message']['mimeType'] == "audio/x-speex":
        Speex.decode(filename)


def remove_first_voice_message():
    """Remove the first message"""
    if len(control.playlist) == 0:
        return

    del control.playlist[0]
    if len(control.playlist) < MIN_MESSAGES_IN_PLAYLIST:
        ServerCommunication.get_playlist()  # get more messages

    elif len(control.playlist) == 0:
        # end of list! Not good...
        log.warn("Playlist is empty, using emergency list!")
        control.playlist = control.emergency_playlist[:]


def playlist_updated():
    """Update the emergency playlist and clear out any old audio files"""
    files = dict()
    for m in control.emergency_playlist:
        log.debug("E: " + m.messageId)
        files[m.messageId] = m.messageId

    for m in control.playlist:
        log.debug("P: " + m.messageId)
        files.pop(m.messageId, None)

    for f in files:
        log.info("Deleting " + get_filename(f))
        os.unlink(get_filename(f))

    control.emergency_playlist = control.playlist[:]
