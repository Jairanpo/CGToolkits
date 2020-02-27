
import os

def outputs(sources, export_path, messages):
    result = {}
    _unc = "UNCOMPRESS"

    for source in sources:
        _video_path = os.path.join(
            export_path,
            source.name,
            source_folder_name(source, mode="video"),
            "FOLDER",
            f"{source.filename}_{source.name}_FILENAME".upper() + ".mov")

        _video_path = os.path.normpath(_video_path)

        _images_path = os.path.join(
            export_path,
            source.name,
            source_folder_name(source, mode="image"),
            "IMAGE_SEQUENCE",
            f"{source.filename}_{source.name}".upper() + "_%04d.png")

        _images_path = os.path.normpath(_images_path)

        if is_valid_setup(source, messages):
            messages.append(
                (f'<img src="./CGAgnostics/icons/check_XS.png"></img> - {source.name} export configuration created.', "success"))
            result[source.name] = {
                "name": source.name,
                "enable": True,
                "source": f'{source.source}',
                "video": {
                    "enable": source.do_export_videos,
                    "QT": {
                        "enable": source.do_export_QT,
                        "output": f'{_video_path.replace("FOLDER", "QT").replace("FILENAME", "QT")}'
                    },
                    "HD": {
                        "enable": source.do_export_HD,
                        "output": f'{_video_path.replace("FOLDER", "HD").replace("FILENAME", "HD")}'
                    },
                    "UNCOMPRESS": {
                        "enable": source.do_export_uncompress,
                        "4444": _video_path.replace("FOLDER", _unc).replace("FILENAME", "4444"),
                        "H264": _video_path.replace("FOLDER", _unc).replace("FILENAME", "H264"),
                        "output": f'{_video_path.replace("FOLDER", "UNCOMPRESS").replace("FILENAME", "UNCOMPRESS")}'
                    }
                },
                "images": {
                    "enable": source.do_export_image_sequence,
                    "output": f'{_images_path}'
                }
            }
        else:
            messages.append(
                (f'<img src="./CGAgnostics/icons/warning_XS.png"></img> - {source.name} export configuration not created.', "warning"))
            result[source.name] = {
                "enable": False,
                "name": source.name
            }

    return result


def is_valid_setup(source, messages):
    result = None

    def is_valid_source():
        if os.path.isfile(source.source):
            messages.append((f'<img src="./CGAgnostics/icons/check_XS.png"></img> - {source.name} source is valid.', "success"))
            return True
        else:
            messages.append((f'<img src="./CGAgnostics/icons/x_XS.png"></img> - {source.name} source is invalid.', "error"))
            return False

    def is_valid_filename():
        if len(source.filename) > 0:
            messages.append((f'<img src="./CGAgnostics/icons/check_XS.png"></img> - {source.name} filename is valid.', "success"))
            return True
        else:
            messages.append((f'<img src="./CGAgnostics/icons/x_XS.png"></img> - {source.name} filename is invalid.', "error"))
            return False

    _is_valid_source = is_valid_source()
    _is_valid_filename = is_valid_filename()

    result = _is_valid_source and _is_valid_filename

    return result


def source_folder_name(source, mode="video"):
    result = ''
    if mode == "video":
        if source.videos_export_directory == "":
            result = "Carpeta 01"
        else:
            result = source.videos_export_directory

    elif mode == "image":
        if source.images_export_directory == "":
            result = "Carpeta 03"
        else:
            result = source.images_export_directory

    return result
