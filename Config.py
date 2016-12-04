import ConfigParser
import os
import errno
import logging

version = "0.1"

# defaults
station_id = "xxxxxxxxxx"
server_url = "http://localhost:8080/"
data_path = "/tmp/iot-client"
recording_time = 15.0
sensor_message_delay = 30.0
vote_post_frequency = 120.0
log_level = "WARNING"

# read config file
config = ConfigParser.RawConfigParser()
config.read("station.config")
try:
    station_id = config.get("Config", "id")
    server_url = config.get("Config", "server")
    data_path = config.get("Config", "data_path")
    recording_time = config.getfloat("Config", "recording_time")
    sensor_message_delay = config.getfloat("Config", "sensor_message_delay")
    vote_post_frequency = config.getfloat("Config", "vote_post_frequency")
    log_level = config.get("Config", "log_level")
except ConfigParser.NoOptionError:
    pass

# create data dir if it doesn't already exist
try:
    os.makedirs(data_path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# setup logging
log_level = getattr(logging, log_level.upper(), None)
if not isinstance(log_level, int):
    raise ValueError('Invalid log level: %s' % log_level)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)s : %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    level=log_level)
