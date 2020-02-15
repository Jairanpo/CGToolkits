
import os

def output_dictionary(sources, export_path, messages):
    result = {}

    for source in sources:
            _video_path = os.path.join(
                export_path,
                source_folder_name(source, mode="video"),
                "FOLDER",
                f"{source.filename}_{source.name}_FILENAME".upper() + ".mov")

            _video_path = os.path.normpath(_video_path)

            _images_path = os.path.join(
                export_path,
                source_folder_name(source, mode="image"),
                "IMAGE_SEQUENCE",
                f"{source.filename}_{source.name}".upper() + "_%04d.png")

            _images_path = os.path.normpath(_images_path)

            if is_valid_setup(source, messages):
                messages.append((f"{source.name} export configuration created.", "success"))
                result[source.name] = {
                    "status": True,
                    "video":{
                        "enable": source.do_export_videos,
                        "QT": {
                            "enable": source.do_export_QT,
                            "filepath": _video_path.replace("FOLDER", "QT").replace("FILENAME", "QT")
                        },
                        "HD": {
                            "enable": source.do_export_HD,
                            "filepath": _video_path.replace("FOLDER", "HD").replace("FILENAME", "HD")
                        },
                        "UNCOMPRESS": {
                            "enable": source.do_export_uncompress,
                            "source": _video_path.replace("FOLDER", "UNCOMPRESS").replace("FILENAME", "UNCOMPRESS"),
                            "4444": _video_path.replace("FOLDER", "UNCOMPRESS").replace("FILENAME", "4444"),
                            "H264": _video_path.replace("FOLDER", "UNCOMPRESS").replace("FILENAME", "H264"),
                        }
                    },
                    "images": {
                        "enable": source.do_export_image_sequence,
                        "filepath": _images_path
                    }
                }
            else:
                messages.append((f"{source.name} export configuration not created.", "warning"))
                result[source.name] = {
                    "status": False
                }


    return result


def is_valid_setup(source, messages):
    result = None

    def is_valid_source():
        if os.path.isfile(source.source):
            messages.append((f"{source.name} source is valid.", "success"))
            return True
        else:
            messages.append((f"{source.name} source is invalid.", "error"))
            return False    

    def is_valid_filename():
        if len(source.filename) > 0:
            messages.append((f"{source.name} filename is valid.", "success"))
            return True
        else:
            messages.append((f"{source.name} filename is invalid.", "error"))
            return False

    _is_valid_source =  is_valid_source()
    _is_valid_filename = is_valid_filename()

    result = _is_valid_source and _is_valid_filename
    
    return result

def source_folder_name(source, mode="video"):
    result = ''
    if mode == "video":
        if source.videos_export_directory == "":
            result = "Carpeta 01"

    elif mode == "image":
        if source.images_export_directory == "":
            result = "Carpeta 03"

    return result
    
        