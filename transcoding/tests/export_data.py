import sys
import os

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

ffmpeg = os.path.abspath(os.getcwd())
ffmpeg = os.path.join(ffmpeg, "transcoding", "ffmpeg", "bin", "ffmpeg.exe")
correct_source = os.path.normpath("C:\\Projects\\CGToolkits\\transcoding\\tests\\videos\\EVE030.mov")
incorrect_source = os.path.normpath("C:\\Projectsa\\CGToolkitsb\\transcodingc\\testsd\\videose\\EVE030f.mov")
correct_output = os.path.normpath("C:\\Projects\\CGToolkits\\transcoding\\tests\\videos\\output.mov")
incorrect_output = os.path.normpath("C:\\Projaects\\CGToolkits\\transcoding\\tests\\videos\\output.mov")
_command_error_message = "Unable to create command."
_filename = "MY_FILE_NAME"


ts01 = {
    "UNCOMPRESS_path":os.path.join(
        "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
        "Carpeta 01",
        "UNCOMPRESS")
}

ts01["UNCOMPRESS"] = os.path.join(
    "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
    "Carpeta 01",
    "UNCOMPRESS",
    f'{_filename}_4444.mov'
)

ts01["4444"] = os.path.join(
    "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
    "Carpeta 01",
    "UNCOMPRESS",
    f'{_filename}_4444.mov'
)

ts01["H264"] = os.path.join(
    "C:\\Projects\\CGToolkits\\transcoding\\tests\\videos",
    "Carpeta 01",
    "UNCOMPRESS",
    f'{_filename}_H264.mov'
)
ts01["QT_path"] = ts01["UNCOMPRESS_path"].replace("UNCOMPRESS", "QT") 
ts01["HD_path"] = ts01["UNCOMPRESS_path"].replace("UNCOMPRESS", "HD") 


ts01["commands"]["H264"] = (f'{ffmpeg} '
                        f'-i {correct_source} '
                        f'-framerate 24 '
                        f'-c:v libx264 '
                        f'-crf 21 '
                        f'-preset "medium" '
                        f'{ts01["H264"]}')

ts01["commands"]["4444"] = (f'{ffmpeg} '
                        f'-i {correct_source} '
                        f'-framerate 24 '
                        f'-i {ts01["UNCOMPRESS"]["source"]} '
                        f'-c:v libx264 '
                        f'-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p" '
                        f'-profile: 4444 ' 
                        f'-crf 21 '
                        f'-preset "medium" '
                        f'{ts01["4444"]}')

ts01["config"]={
    'status': True,
    'source': correct_source,  
    'video': {
        'enable': True, 
        'QT': {
            'enable': True, 
            'filepath': ts01["QT_path"]
        }, 
        'HD': {
            'enable': True, 
            'filepath': ts01["HD_path"]
            }, 
        'UNCOMPRESS': {
            'enable': True,
            '4444': ts01["4444"], 
            'H264': ts01["H264"],
            "path": ts01["UNCOMPRESS_path"]
        },
    }, 
    'images': {
        'enable': False, 
    }
}

ts01["copy_QT"] = f'copy {ts01["UNCOMPRESS_path"]} {ts01["QT_path"]}'
ts01["copy_HD"] = f'copy {ts01["UNCOMPRESS_path"]} {ts01["HD_path"]}'
