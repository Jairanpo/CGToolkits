import sys
import os
import subprocess

ffmpeg = os.path.abspath(os.getcwd())
ffmpeg = f'{os.path.join(ffmpeg,"ffmpeg", "bin", "ffmpeg.exe")}'



def video(config, ffmpeg=ffmpeg):
    _cmd = []
    _cmd.append(ffmpeg)
   
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
        _cmd.append('-n')
    elif config["force"] == True:
        ffmpeg += ' ' + '-y'
        _cmd.append('-y')
    elif config["force"] == False:
        ffmpeg += ' ' + '-n'
        _cmd.append('-n')

    # Framerate:
    '''
    if "framerate" in config:
        ffmpeg += ' ' + f'-framerate {config["framerate"]}'
        _cmd.append('-framerate')
        _cmd.append(f'{config["framerate"]}')
    else:
        ffmpeg += ' ' + f'-framerate 24'  # Default to 24
        _cmd.append('-framerate')
        _cmd.append("24")
    '''

    # Inputs:
    if os.path.isfile(config["source"]):
        ffmpeg += ' ' + f'-i "{config["source"]}"'
        _cmd.append('-i')
        _cmd.append(config["source"])
    else:
        result = {
            "command": _command_error_message,
            "valid": False,
            "message": ["Invalid video source file.", "error"]}
        return result

    # Filter
    if "filter" in config:
        ffmpeg += ' ' + f'-vf \"{config["filter"]}\"'
        _cmd.append('-vf')
        _cmd.append(config["filter"])

    # Codec:
    if "codec" in config:
        ffmpeg += ' ' + f'-c:v {config["codec"]}'
        _cmd.append('-c:v')
        _cmd.append(config["codec"])
    else:
        ffmpeg += ' ' + '-c:v libx264'  # Default to H264
        _cmd.append('-c:v')
        _cmd.append('libx264')

    # Profile:
    if "profile" in config:
        ffmpeg += ' ' + f'-profile:v {config["profile"]}'
        _cmd.append('-profile:v')
        _cmd.append(f'{config["profile"]}')

    # Constant rate factor:
    if "crf" in config:
        ffmpeg += ' ' + f'-crf {config["crf"]}'
        _cmd.append('-crf')
        _cmd.append(f'{config["crf"]}')
    else:
        ffmpeg += ' ' + '-crf 21'  # Default to 21
        _cmd.append('-crf')
        _cmd.append("21")

    # Preset:
    if "preset" in config:
        ffmpeg += ' ' + f'-preset "{config["preset"]}"'
        _cmd.append('-preset')
        _cmd.append(config["preset"])
    else:
        ffmpeg += ' ' + f'-preset "medium"'  # Default to medium
        _cmd.append('-preset')
        _cmd.append('medium')

    # Output:
    if "output" in config:
        path, filename = os.path.split(
            os.path.abspath(config["output"].strip()))
        if os.path.exists(path):
            ffmpeg += ' ' + f'"{config["output"]}"'
            _cmd.append(config["output"])
            result = {
                "composed": _cmd,
                "command": ffmpeg,
                "valid": True,
                "message": [f"ffmpeg command created succesfully for {filename}", "success"]
            }
            return result
        else:
            result = {
                "valid": False,
                "message": [f'Invalid output directory: {config["output"]}', "error"],
                "command": _command_error_message,
                "composed": _command_error_message
            }
    else:
        result = {
            "valid": False,
            "message": ["Output directory not set.", "error"],
            "command": _command_error_message,
            "composed": _command_error_message
        }

    return result

def image_sequence(config, ffmpeg=ffmpeg):
    _cmd = []
    _cmd.append(ffmpeg)
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
        _cmd.append('-n')
    elif config["force"] == True:
        ffmpeg += ' ' + '-y'
        _cmd.append('-y')
    elif config["force"] == False:
        ffmpeg += ' ' + '-n'
        _cmd.append('-n')

    # Inputs:
    if os.path.isfile(config["source"]):
        ffmpeg += ' ' + f'-i {config["source"]}'
        _cmd.append('-i')
        _cmd.append(config["source"])
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
            _cmd.append(config["output"])
            result = {
                "command": ffmpeg,
                "composed": _cmd,
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
