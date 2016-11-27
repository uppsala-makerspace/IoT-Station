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
with open('station.config', 'w') as f:
    config.write(f)

print "Done!"
