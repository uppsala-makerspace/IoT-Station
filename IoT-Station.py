import ServerCommunication
import Votes
import Audio
import Playlist
import Raspberry
import sys


def main():
    # say hello
    ServerCommunication.ping_server()

    # get playlist
    ServerCommunication.get_playlist()
    Playlist.control.play()

    # start the vote submit timer
    Votes.post_votes()

    Raspberry.setup()

    # Raspberry.record_callback()

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



