import ServerCommunication
import Votes
import Audio
import Playlist
import Raspberry
import time
import sys


def main():
    # say hello
    ServerCommunication.ping_server()

    # get playlist
    ServerCommunication.get_playlist()
    Playlist.control.play()

    Raspberry.setup()

#   TODO: need to periodically call post_votes
    # ServerCommunication.post_votes()
    # print Votes.get_json()

    while 1:
        """"""
        # time.sleep(0.5)
        # print "ping"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        Audio.control.stop_sound()
        Playlist.control.stop()
        sys.exit(0)



