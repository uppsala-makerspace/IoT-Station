import subprocess
import ConfigParser

print "Setup..."
subprocess.call("pip install Requests", shell=True)
subprocess.call("pip install pyaudio", shell=True)

# create default config file
config = ConfigParser.RawConfigParser()
config.add_section("Config")
config.set("Config", "id", "xxxxxxxxxx")
config.set("Config", "server", "http://localhost:8080/")
config.set("Config", "data_path", "/tmp/iot-client")
config.set("Config", "recording_time", 15)
config.set("Config", "sensor_message_delay", 30)
config.set("Config", "vote_post_frequency", 120)
with open('station.config', 'w') as f:
    config.write(f)

print "Done!"
