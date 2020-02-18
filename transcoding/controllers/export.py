import controllers.encode 

def is_export_video_enabled(source):
    if source["video"]["enable"]:
        return True
    else:
        return False

def is_export_UNCOMPRESS_enabled(source):
    if source["video"]["UNCOMPRESS"]["enable"]:
        return True
    else:
        return False

def is_export_QT_enabled(source):
    if source["video"]["QT"]["enable"]:
        return True
    else:
        return False

def is_export_HD_enabled(source):
    if source["video"]["HD"]["enable"]:
        return True
    else:
        return False



def with_sources(list_of_sources):
    '''
        list_of_sources = [{
            "status": <Boolean>,
            "video":{
                "enable": <Boolean>,
                "QT": {
                    "enable": <Boolean>,
                    "filepath": <filepath>
                },
                "HD": {
                    "enable": <Boolean>,
                    "filepath": <filepath>
                },
                "UNCOMPRESS": {
                    "enable": <Boolean>,
                    "source": <filepath>,
                    "4444": <filepath>,
                    "H264": <filepath>,
                }
            },
            "images": {
                "enable": <Boolean>,
                "filepath": <filepath>
            }
        }, ]
    '''

    result = {}
    _transcoding_config = {
        "4444": {
            "force": True, 
            "framerate": 24,
            "codec": "prores_ks",
            "profile": 4444,
            "filter": "pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p",
        },
        "H264":{
            "force": True, 
            "framerate": 24,
            "codec": "libx264"
        }
    }

    for source in list_of_sources:
        
        if source["status"]:

            # Setting the source and output for the H264 and 4444 config dictionaries: 
            _transcoding_config["H264"]["source"] = source["source"]
            _transcoding_config["4444"]["source"] = source["source"]
            _transcoding_config["4444"]["output"] = source["UNCOMPRESS"]["4444"]
            _transcoding_config["H264"]["output"] = source["UNCOMPRESS"]["H264"]
            _transcoding_config["UNCOMPRESS"]["path"] = source["UNCOMPRESS"]["path"]
            
            if is_export_UNCOMPRESS_enabled(source):
                os.makedirs(_transcoding_config["UNCOMPRESS"]["path"])
                result["4444"] = enconde.command(_transcoding_config["4444"])
                result["H264"] = enconde.command(_transcoding_config["H264"])

                if is_export_QT_enabled(source):
                    result["QT"] = f'copy {transcoding_config["H264"]["source"]} {source["QT"]["filepath"]}'
                else:
                    pass

                if is_export_HD_enabled(source):
                    result["HD"] = f'copy {transcoding_config["H264"]["source"]} {source["HD"]["filepath"]}'
                else:
                    pass

            else:
                if is_export_QT_enabled(source) and not is_export_HD_enabled(source):
                    os.makedirs(os.path.dirname(source["QT"]["filepath"]))
                    result["QT"] = enconde.command(_transcoding_config["H264"])

                elif is_export_QT_enabled(source) and is_export_HD_enabled(source):
                    os.makedirs(os.path.dirname(source["HD"]["filepath"]))
                    result["HD"] = enconde.command(_transcoding_config["H264"])
        else:
            result.append(["No video was exported", "standar"])

    return result