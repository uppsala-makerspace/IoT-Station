import subprocess
import base64
import os


def encode(filename):
    """Encode speex data and return the base64 encoded string"""
    subprocess.call("speexenc " + filename + ".wav " + filename + ".spx")

    with open(filename + ".spx", "rb") as f:
        base64data = base64.b64encode(f.read())

    return base64data


def decode(filename):
    """Decode speex data to wav file and remove the spx file"""
    subprocess.call("speexdec " + filename + ".spx " + filename + ".wav")
    os.unlink(filename + ".spx")
