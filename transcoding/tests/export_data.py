export_all = {
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


do_not_export = {
    "status": False
}


export_video_alone = {
    "status": True,
    "video":{
        "enable": source.do_export_videos,
        "QT": {
            "enable": False,
            "filepath": _video_path.replace("FOLDER", "QT").replace("FILENAME", "QT")
        },
        "HD": {
            "enable": False,
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
        "enable": False,
        "filepath": _images_path
    }
}