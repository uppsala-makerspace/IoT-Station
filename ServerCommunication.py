import requests
import base64
import Config
import Votes
import Playlist
import Speex


def ping_server():
    """Ping the server"""
    headers = {'X-Station-ID': Config.station_id}
    req = requests.get(Config.server_url + 'api/v1/ping', headers=headers)
    print req.text


def post_audio_message(filename):
    """Upload an audio file to the server"""
    headers = {'X-Station-ID': Config.station_id}

    base64data = Speex.encode(filename)
    data = {'base64Data': base64data, 'mimeType': 'audio/x-speex'}

    req = requests.post(Config.server_url + 'api/v1/message', headers=headers, json=data)
    print req.text


def post_votes():
    """Post voting list to server"""
    headers = {'X-Station-ID': Config.station_id, 'Content-type': 'application/json'}

    # no votes stored!
    if len(Votes.votes) == 0:
        print "No votes to upload"
        return

    req = requests.post(Config.server_url + 'api/v1/vote', headers=headers, data=Votes.get_json())

    print req.text

    # delete the votes
    Votes.clear_votes()


def get_playlist():
    """Get a playlist from the server"""
    headers = {'X-Station-ID': Config.station_id}
    params = {'amount': 4}  # TODO: only requesting 4 voice messages right now, should be more!

    req = requests.get(Config.server_url + 'api/v1/playlist', headers=headers, params=params)

    for m in req.json():
        Playlist.add_voice_message(m)

    Playlist.playlist_updated()
    # print json.dumps(req.json(), sort_keys=True, indent=4, separators=(',', ': '))
