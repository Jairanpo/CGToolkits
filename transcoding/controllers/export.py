import os
import transcoding.controllers.encode as encode


def created(format, status, created=True):
    if created:
        return {
            "valid": True,
            "message": [f"{format} command was created", status]
        }
    else:
        return {
            "valid": False,
            "message": [f"{format} command was not created", status]
        }


def with_source(source):
    '''
        list_of_sources = [{
            "enable": <Boolean>,
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
            "source": source["source"],
            "codec": "prores_ks",
            "profile": 4444,
            "filter": "pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p",
            "output": source["video"]["UNCOMPRESS"]["4444"]
        },
        "H264": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "libx264",
            "output": source["video"]["UNCOMPRESS"]["H264"]
        },
        "UNCOMPRESS": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "libx264",
            "preset": "ultrafast",
            "output": source["video"]["UNCOMPRESS"]["output"]
        },
        "QT": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "libx264",
            "preset": "ultrafast",
            "output": source["video"]["QT"]["output"]
        },
        "HD": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "libx264",
            "preset": "ultrafast",
            "output": source["video"]["HD"]["output"]
        },
        "PNG": {
            "force": True,
            "source": source["source"],
            "output": source["images"]["output"]
        }
    }

    if source["video"]["UNCOMPRESS"]["enable"]:
            # Setting the source and output for the H264 and 4444 config dictionaries:

        result["4444"] = created("4444", "success")
        result["4444"]["command"] = encode.video(
            _transcoding_config["4444"])["command"]

        result["H264"] = created("H264", "success")
        result["H264"]["command"] = encode.video(
            _transcoding_config["H264"])["command"]

        result["UNCOMPRESS"] = created("UNCOMPRESS", "success")
        result["UNCOMPRESS"]["command"] = encode.video(
            _transcoding_config["UNCOMPRESS"])["command"]

# Create with UNCOMPRESS, QT and HD ----------------------------------------------------------------------
        if source["video"]["QT"]["enable"]:
            result["QT"] = created("QT", "success")
            result["QT"]["command"] = f'copy {_transcoding_config["H264"]["output"]} {source["video"]["QT"]["output"]}'
        else:
            result["QT"] = created("QT", "warning", created=False)

        if source["video"]["HD"]["enable"]:
            result["HD"] = created("HD", "success")
            result["HD"]["command"] = f'copy {_transcoding_config["H264"]["output"]} {source["video"]["HD"]["output"]}'
        else:
            result["HD"] = created("HD", "warning", created=False)


# Create without UNCOMPRESS but with QT and HD ----------------------------------------------------------
    elif not source["video"]["UNCOMPRESS"]["enable"] and (source["video"]["QT"]["enable"] and source["video"]["HD"]["enable"]):
        result["QT"] = encode.video(_transcoding_config["QT"])
        result["HD"] = encode.video(_transcoding_config["HD"])
        result["QT"] = created("QT", "success")
        result["HD"] = created("HD", "success")
        result["UNCOMPRESS"] = created("UNCOMPRESS", "warning", created=False)
        result["H264"] = created("H264", "warning", created=False)
        result["4444"] = created("4444", "warning", created=False)


# Create without UNCOMPRESS and HD but with QT ----------------------------------------------------------
    elif (not source["video"]["UNCOMPRESS"]["enable"] and not source["video"]["HD"]["enable"]) and source["video"]["QT"]["enable"]:
        result["QT"] = encode.video(_transcoding_config["QT"])
        result["HD"] = created("HD", "warning", created=False)
        result["UNCOMPRESS"] = created("UNCOMPRESS", "warning", created=False)
        result["H264"] = created("H264", "warning", created=False)
        result["4444"] = created("4444", "warning", created=False)


# Create without UNCOMPRESS and QT but with HD ----------------------------------------------------------
    elif (not source["video"]["UNCOMPRESS"]["enable"] and not source["video"]["QT"]["enable"]) and source["video"]["HD"]["enable"]:
        result["HD"] = encode.video(_transcoding_config["HD"])
        result["QT"] = created("QT", "warning", created=False)
        result["UNCOMPRESS"] = created("UNCOMPRESS", "warning", created=False)
        result["H264"] = created("H264", "warning", created=False)
        result["4444"] = created("4444", "warning", created=False)


# Create without UNCOMPRESS, QT and HD ----------------------------------------------------------
    else:
        result["HD"] = created("HD", "warning", created=False)
        result["QT"] = created("QT", "warning", created=False)
        result["UNCOMPRESS"] = created("UNCOMPRESS", "warning", created=False)
        result["H264"] = created("H264", "warning", created=False)
        result["4444"] = created("4444", "warning", created=False)

    if source["images"]["enable"]:
        result["PNG"] = encode.image_sequence(_transcoding_config["PNG"])
    else:
        result["PNG"] = created("PNG", "warning", created=False)

    return result
