import requests
import Config
import Votes
import Playlist
import Speex
from threading import Timer

import logging
log = logging.getLogger("ServerCommunication")


def ping_server():
    """Ping the server"""
    headers = {'X-Station-ID': Config.station_id}
    try:
        req = requests.get(Config.server_url + 'api/v1/ping', headers=headers)
        log.debug(req.text)
    except requests.ConnectionError as e:
        log.error("No ping response!")
        log.debug(e)


def post_audio_message(filename):
    """Upload an audio file to the server"""
    headers = {'X-Station-ID': Config.station_id}

    base64data = Speex.encode(filename)
    data = {'base64Data': base64data, 'mimeType': 'audio/x-speex'}

    try:
        req = requests.post(Config.server_url + 'api/v1/message', headers=headers, json=data)
        log.debug(req.text)
    except requests.ConnectionError as e:
        # TODO: currently we'll lose this message if we can't get to the server!
        # Should we cache it and try again later?

        log.error("Failed to post audio message!")
        log.debug(e)


def post_votes():
    """Post voting list to server"""
    headers = {'X-Station-ID': Config.station_id, 'Content-type': 'application/json'}

    # no votes stored!
    if len(Votes.votes) == 0:
        log.info("No votes to upload")
        return

    try:
        req = requests.post(Config.server_url + 'api/v1/vote', headers=headers, data=Votes.get_json())
        log.debug(req.text)

        # delete the votes after they've been properly sent
        Votes.clear_votes()
    except requests.ConnectionError as e:
        log.error("Failed to post votes!")
        log.debug(e)


def get_playlist():
    """Get a playlist from the server"""
    headers = {'X-Station-ID': Config.station_id}
    params = {'amount': 4}  # TODO: only requesting 4 voice messages right now, should be more!

    try:
        req = requests.get(Config.server_url + 'api/v1/playlist', headers=headers, params=params)

        for m in req.json():
            Playlist.add_voice_message(m)

        Playlist.playlist_updated()
        # print json.dumps(req.json(), sort_keys=True, indent=4, separators=(',', ': '))
    except requests.ConnectionError as e:
        log.error("Failed to get playlist!")
        log.debug(e)

        # If the current playlist is empty, we have to schedule
        # another try at getting it from the server.
        if len(Playlist.control.playlist) is 0:
            log.error("Playlist is empty! Trying again in 30 seconds...")
            t = Timer(30, get_playlist)
            t.start()
