import Config
import ServerCommunication
import Votes
import Audio
import Playlist
import Raspberry
import sys
# import time
import logging
log = logging.getLogger("main")


def main():
    print ("Starting IoT-Station version: " + Config.version)

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
        log.warn("Interrupted by keyboard")
        Audio.control.stop_sound()
        Playlist.control.stop()
        sys.exit(0)



