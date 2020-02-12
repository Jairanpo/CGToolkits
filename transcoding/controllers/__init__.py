import sys
import os
import subprocess

ffmpeg = os.path.abspath(os.getcwd())
ffmpeg = os.path.join(ffmpeg, "transcoding", "ffmpeg", "bin", "ffmpeg.exe")


def video(config):
    '''
    config = {
        "force": True, 
        "framerate": 24,
        "source": <file path>,
        "codec": "libx264",
        "profile": "4444",
        "crf": 21, 
        "preser": "ultrafast",
        "output": <file path>
    }
    '''
    print(ffmpeg)
