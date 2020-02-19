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


case["QT"] = {
    "valid": True,
    "message": ['ffmpeg command created succesfully for MY_FILE_NAME_QT.mov', 'success'],
    "command": (f'{ffmpeg} '
                f'-y '
                f'-framerate 24 '
                f'-i {correct_source} '
                f'-c:v libx264 '
                f'-crf 21 '
                f'-preset "ultrafast" '
                f'{case["outputs"]["QT"]}'
                )
}

case["UNCOMPRESS"] = {
    "valid": False,
    "message": ["UNCOMPRESS command was not created", "warning"]
}

case["H264"] = {
    "valid": False,
    "message": ["H264 command was not created", "warning"]
}

case["4444"] = {
    "valid": False,
    "message": ["4444 command was not created", "warning"]
}


case["HD"] = {
    "valid": False,
    "message": ["HD command was not created", "warning"]
}

case["config"] = {
    'status': True,
    'source': correct_source,
    'video': {
        'enable': True,
        'QT': {
            'enable': True,
            'output': case["outputs"]["QT"]
        },
        'HD': {
            'enable': False,
            'output': case["outputs"]["HD"]
        },
        'UNCOMPRESS': {
            'enable': False,
            '4444': case["outputs"]["4444"],
            'H264': case["outputs"]["H264"],
            "output": case["outputs"]["UNCOMPRESS"]
        },
    },
    'images': {
        'enable': False,
    }}
