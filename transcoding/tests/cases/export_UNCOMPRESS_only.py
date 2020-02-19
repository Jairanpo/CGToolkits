import sys
import os

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

ffmpeg = os.path.abspath(os.getcwd())
ffmpeg = os.path.join(ffmpeg, "transcoding", "ffmpeg", "bin", "ffmpeg.exe")
correct_source = os.path.normpath(
    "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos\\EVE030.mov")
incorrect_source = os.path.normpath(
    "C:\\Projectsa\\CGToolkitsb\\transcodingc\\testsd\\videose\\EVE030f.mov")
correct_output = os.path.normpath(
    "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos\\output.mov")
incorrect_output = os.path.normpath(
    "C:\\Projaects\\CGToolkits\\transcoding\\tests\\videos\\output.mov")
_command_error_message = "Unable to create command."
_filename = "MY_FILE_NAME"

case = {
    "outputs": {
        "UNCOMPRESS": os.path.join(
            "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
            "Carpeta 01",
            "UNCOMPRESS",
            f'{_filename}_UNCOMPRESS.mov'),

        "4444": os.path.join(
            "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
            "Carpeta 01",
            "UNCOMPRESS",
            f'{_filename}_4444.mov'
        ),

        "H264": os.path.join(
            "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
            "Carpeta 01",
            "UNCOMPRESS",
            f'{_filename}_H264.mov'
        ),

        "QT": os.path.join(
            "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
            "Carpeta 01",
            "QT",
            f'{_filename}_QT.mov'
        ),

        "HD": os.path.join(
            "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
            "Carpeta 01",
            "HD",
            f'{_filename}_HD.mov'
        )
    }}

case["config"] = {
    'status': True,
    'source': correct_source,
    'video': {
        'enable': True,
        'QT': {
            'enable': False,
            'output': case["outputs"]["QT"]
        },
        'HD': {
            'enable': False,
            'output': case["outputs"]["HD"]
        },
        'UNCOMPRESS': {
            'enable': True,
            '4444': case["outputs"]["4444"],
            'H264': case["outputs"]["H264"],
            "output": case["outputs"]["UNCOMPRESS"]
        },
    },
    'images': {
        'enable': False,
    }}

case["UNCOMPRESS"] = {
    "valid": True,
    "message": ["UNCOMPRESS command was created", "success"],
    "command": (f'{ffmpeg} '
                f'-y '
                f'-framerate 24 '
                f'-i {correct_source} '
                f'-c:v libx264 '
                f'-crf 21 '
                f'-preset "ultrafast" '
                f'{case["outputs"]["UNCOMPRESS"]}'
                )
}

case["H264"] = {
    "valid": True,
    "message": ["H264 command was created", "success"],
    "command": (f'{ffmpeg} '
                f'-y '
                f'-framerate 24 '
                f'-i {correct_source} '
                f'-c:v libx264 '
                f'-crf 21 '
                f'-preset "medium" '
                f'{case["outputs"]["H264"]}'
                )
}

case["4444"] = {
    "valid": True,
    "message": ["4444 command was created", "success"],
    "command": (f'{ffmpeg} '
                f'-y '
                f'-framerate 24 '
                f'-i {correct_source} '
                f'-vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p\" '
                f'-c:v prores_ks '
                f'-profile:v 4444 '
                f'-crf 21 '
                f'-preset "medium" '
                f'{case["outputs"]["4444"]}'
                )}

case["QT"] = {
    "valid": False,
    "message": ["QT command was not created", "warning"]
}

case["HD"] = {
    "valid": False,
    "message": ["HD command was not created", "warning"]
}
