import ConfigParser
import os
import errno

config = ConfigParser.RawConfigParser()
config.read("station.config")
station_id = config.get("Config", "id")
server_url = config.get("Config", "server")
data_path = config.get("Config", "data_path")
recording_time = config.getfloat("Config", "recording_time")
sensor_message_delay = config.getfloat("Config", "sensor_message_delay")
vote_post_frequency = config.getfloat("Config", "vote_post_frequency")

# create data dir if it doesn't already exist
try:
    os.makedirs(data_path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
