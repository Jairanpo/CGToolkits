import sys
import os
import subprocess

ffmpeg = os.path.abspath(os.getcwd())
ffmpeg = os.path.join(ffmpeg, "transcoding", "ffmpeg", "bin", "ffmpeg.exe")

def video(config, ffmpeg=ffmpeg):
   
    _command_error_message = "Unable to create command."
    '''
    config = {
        "force": True, 
        "framerate": 24,
        "source": <file path>,
        "filter": "pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p"
        "codec": "libx264",
        "profile": "4444",
        "crf": 21, 
        "preset": "ultrafast",
        "output": <file path>
    }
    '''
    _message = []
    result = {"valid": False, "message": _message.append(
        ["Unable to create your ffmpeg configuration.", "error"])}

    # Force overwrite:

    if "force" not in config:
        ffmpeg += ' ' + '-n'  # Default to not overwrite
    elif config["force"] == True:
        ffmpeg += ' ' + '-y'
    elif config["force"] == False:
        ffmpeg += ' ' + '-n'

    # Framerate:
    if "framerate" in config:
        ffmpeg += ' ' + f'-framerate {config["framerate"]}'
    else:
        ffmpeg += ' ' + f'-framerate 24'  # Default to 24

    # Inputs:
    if os.path.isfile(config["source"]):
        ffmpeg += ' ' + f'-i {config["source"]}'
    else:
        result = {
            "command": _command_error_message,
            "valid": False,
            "message": ["Invalid video source file.", "error"]}
        return result

    # Filter
    if "filter" in config:
        ffmpeg += ' ' + f'-vf \"{config["filter"]}\"'

    # Codec:
    if "codec" in config:
        ffmpeg += ' ' + f'-c:v {config["codec"]}'
    else:
        ffmpeg += ' ' + '-c:v libx264'  # Default to H264

    # Profile:
    if "profile" in config:
        ffmpeg += ' ' + f'-profile:v {config["profile"]}'

    # Constant rate factor:
    if "crf" in config:
        ffmpeg += ' ' + f'-crf {config["crf"]}'
    else:
        ffmpeg += ' ' + '-crf 21'  # Default to 21

    # Preset:
    if "preset" in config:
        ffmpeg += ' ' + f'-preset "{config["preset"]}"'
    else:
        ffmpeg += ' ' + f'-preset "medium"'  # Default to medium

    # Output:
    if "output" in config:
        path, filename = os.path.split(
            os.path.abspath(config["output"].strip()))
        if os.path.exists(path):
            ffmpeg += ' ' + f'{config["output"]}'
            result = {
                "command": ffmpeg,
                "valid": True,
                "message": [f"ffmpeg command created succesfully for {filename}", "success"]
            }
            return result
        else:
            result = {
                "valid": False,
                "message": [f'Invalid output directory: {config["output"]}', "error"],
                "command": _command_error_message
            }
    else:
        result = {
            "valid": False,
            "message": ["Output directory not set.", "error"],
            "command": _command_error_message
        }

    return result

def image_sequence(config, ffmpeg=ffmpeg):
   
    _command_error_message = "Unable to create command."
    '''
    config = {
        "source": <file path>,
        "output": <file path>
    }
    '''
    _message = []
    result = {"valid": False, "message": _message.append(
        ["Unable to create your ffmpeg configuration.", "error"])}

    # Force overwrite:

    if "force" not in config:
        ffmpeg += ' ' + '-n'  # Default to not overwrite
    elif config["force"] == True:
        ffmpeg += ' ' + '-y'
    elif config["force"] == False:
        ffmpeg += ' ' + '-n'

    # Inputs:
    if os.path.isfile(config["source"]):
        ffmpeg += ' ' + f'-i {config["source"]}'
    else:
        result = {
            "command": _command_error_message,
            "valid": False,
            "message": ["Invalid video source file.", "error"]}
        return result

    # Output:
    if "output" in config:
        path, filename = os.path.split(
            os.path.abspath(config["output"].strip()))
        if os.path.exists(path):
            ffmpeg += ' ' + f'{config["output"]}'
            result = {
                "command": ffmpeg,
                "valid": True,
                "message": [f"ffmpeg command created succesfully for {filename}", "success"]
            }
            return result
        else:
            result = {
                "valid": False,
                "message": [f'Invalid output directory: {config["output"]}', "error"],
                "command": _command_error_message
            }
    else:
        result = {
            "valid": False,
            "message": ["Output directory not set.", "error"],
            "command": _command_error_message
        }

    return result
