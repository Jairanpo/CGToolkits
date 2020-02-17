import os

ffmpeg = os.path.abspath(os.getcwd())
ffmpeg = os.path.join(ffmpeg, "transcoding", "ffmpeg", "bin", "ffmpeg.exe")
correct_source = os.path.normpath("C:\\Projects\\CGToolkits\\transcoding\\tests\\videos\\EVE030.mov")
incorrect_source = os.path.normpath("C:\\Projectsa\\CGToolkitsb\\transcodingc\\testsd\\videose\\EVE030f.mov")
correct_output = os.path.normpath("C:\\Projects\\CGToolkits\\transcoding\\tests\\videos\\output.mov")
incorrect_output = os.path.normpath("C:\\Projaects\\CGToolkits\\transcoding\\tests\\videos\\output.mov")
_command_error_message = "Unable to create command."

# Everything correct 
test_01= {
    "config":{
    "force": True, 
    "framerate": 24,
    "source": correct_source,
    "codec": "libx264",
    "profile": "4444",
    "crf": 30, 
    "preset": "ultrafast",
    "output": correct_output}
    }

test_01["command"] = (f"{ffmpeg} -y "
                    f'-framerate {test_01["config"]["framerate"]} '
                    f'-i {correct_source} '
                    f'-c:v \"libx264\" '
                    f'-profile:v "{test_01["config"]["profile"]}" ' 
                    f'-crf 30 -preset "{test_01["config"]["preset"]}" '
                    f'{correct_output}')

# Invalid source 
test_02 = {
    "config":{
    "force": True, 
    "framerate": 30,
    "source": incorrect_source,
    "codec": "",
    "profile": "",
    "crf": 30, 
    "preset": "ultrafast",
    "output": correct_output
    },
    "message":  ["Invalid video source file.", "error"],
    "valid": False,
    "command": _command_error_message}

# Invalid output 
test_03 = {
    "config":{
    "force": True, 
    "framerate": 13,
    "source": correct_source,
    "codec": "",
    "profile": "",
    "crf": 50, 
    "preset": "ultrafast",
    "output": incorrect_output
    },
    "message":  ["Invalid output directory.", "error"],
    "valid": False,
    "command": _command_error_message}


# Without framerate
test_04= {
    "config":{
    "force": True, 
    "source": correct_source,
    "codec": "libx264",
    "profile": "4444",
    "crf": 100, 
    "preset": "medium",
    "output": correct_output}}

test_04["command"] = (f"{ffmpeg} -y " 
                    f"-framerate 24 " 
                    f"-i {correct_source} "
                    f'-c:v "libx264" '
                    f'-profile:v "{test_04["config"]["profile"]}" ' 
                    f'-crf {test_04["config"]["crf"]} '
                    f'-preset "{test_04["config"]["preset"]}" '
                    f'{correct_output}')

# Without force
test_05= {
    "config":{
    "framerate": 24,
    "source": correct_source,
    "codec": "libx264",
    "profile": "4444",
    "crf": 30, 
    "preset": "ultrafast",
    "output": correct_output}
    }

test_05["command"] = (f"{ffmpeg} -n "
                    f'-framerate {test_05["config"]["framerate"]} '
                    f'-i {correct_source} '
                    f'-c:v \"libx264\" '
                    f'-profile:v "{test_05["config"]["profile"]}" ' 
                    f'-crf 30 -preset "{test_05["config"]["preset"]}" '
                    f'{correct_output}')


# Without crf
test_06= {
    "config":{
    "framerate": 24,
    "source": correct_source,
    "codec": "libx264",
    "profile": "4444",
    "preset": "ultrafast",
    "output": correct_output}
    }

test_06["command"] = (f"{ffmpeg} -n "
                    f'-framerate {test_06["config"]["framerate"]} '
                    f'-i {correct_source} '
                    f'-c:v \"libx264\" '
                    f'-profile:v "{test_06["config"]["profile"]}" ' 
                    f'-crf 21 -preset "{test_06["config"]["preset"]}" '
                    f'{correct_output}')



# without preset
test_07= {
    "config":{
    "force": True, 
    "framerate": 24,
    "source": correct_source,
    "codec": "libx264",
    "profile": "4444",
    "crf": 30, 
    "output": correct_output}
    }

test_07["command"] = (f"{ffmpeg} -y "
                    f'-framerate {test_07["config"]["framerate"]} '
                    f'-i {correct_source} '
                    f'-c:v \"libx264\" '
                    f'-profile:v "{test_07["config"]["profile"]}" ' 
                    f'-crf 30 -preset "medium" '
                    f'{correct_output}')



