import os

import controllers.encode as encode


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
    if "source" not in source:
        return {"enable": False, "message": ["No source key provided", "error"]}

    result = {}
    _transcoding_config = {
        "4444": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "prores_ks",
            "profile": 4444,
            "filter": 'pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p',
            "output": source["video"]["UNCOMPRESS"]["4444"]
        },
        "H264": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "libx264",
            "filter": 'pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p',
            "output": source["video"]["UNCOMPRESS"]["H264"]
        },
        "UNCOMPRESS": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "codec": "libx264",
            "filter": 'pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p',
            "preset": "ultrafast",
            "output": source["video"]["UNCOMPRESS"]["output"]
        },
        "QT": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "filter": 'pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p',
            "codec": "libx264",
            "preset": "ultrafast",
            "output": source["video"]["QT"]["output"]
        },
        "HD": {
            "force": True,
            "framerate": 24,
            "source": source["source"],
            "filter": 'pad=ceil(iw/2)*2:ceil(ih/2)*2, format=yuv420p',
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
        result["4444"] = encode.video(
            _transcoding_config["4444"])
        result["4444"]["mode"] = "ffmpeg"

        result["H264"] = created("H264", "success")
        result["H264"] = encode.video(
            _transcoding_config["H264"])
        result["H264"]["mode"] = "ffmpeg"

        result["UNCOMPRESS"] = created("UNCOMPRESS", "success")
        result["UNCOMPRESS"] = encode.video(
            _transcoding_config["UNCOMPRESS"])
        result["UNCOMPRESS"]["mode"] = "ffmpeg"

# Create with UNCOMPRESS, QT and HD ----------------------------------------------------------------------
        if source["video"]["QT"]["enable"]:
            result["QT"] = created("QT", "success")
            result["QT"]["composed"] = [_transcoding_config["H264"]["output"], source["video"]["QT"]["output"]]
            result["QT"]["mode"] = "copy"
        else:
            result["QT"] = created("QT", "warning", created=False)

        if source["video"]["HD"]["enable"]:
            result["HD"] = created("HD", "success")
            result["HD"]["composed"] = [_transcoding_config["H264"]["output"], source["video"]["HD"]["output"]]
            result["HD"]["mode"] = "copy"
        else:
            result["HD"] = created("HD", "warning", created=False)


# Create without UNCOMPRESS but with QT and HD ----------------------------------------------------------
    elif not source["video"]["UNCOMPRESS"]["enable"] and (source["video"]["QT"]["enable"] and source["video"]["HD"]["enable"]):
        result["QT"] = encode.video(_transcoding_config["QT"])
        result["QT"]["mode"] = "ffmpeg"
        result["HD"] = created("HD", "success")
        result["HD"]["composed"] = [_transcoding_config["QT"]["output"], source["video"]["HD"]["output"]]
        result["HD"]["mode"] = "copy"
        result["UNCOMPRESS"] = created("UNCOMPRESS", "warning", created=False)
        result["H264"] = created("H264", "warning", created=False)
        result["4444"] = created("4444", "warning", created=False)


# Create without UNCOMPRESS and HD but with QT ----------------------------------------------------------
    elif (not source["video"]["UNCOMPRESS"]["enable"] and not source["video"]["HD"]["enable"]) and source["video"]["QT"]["enable"]:
        result["QT"] = encode.video(_transcoding_config["QT"])
        result["QT"]["mode"] = "ffmpeg"
        result["HD"] = created("HD", "warning", created=False)
        result["UNCOMPRESS"] = created("UNCOMPRESS", "warning", created=False)
        result["H264"] = created("H264", "warning", created=False)
        result["4444"] = created("4444", "warning", created=False)


# Create without UNCOMPRESS and QT but with HD ----------------------------------------------------------
    elif (not source["video"]["UNCOMPRESS"]["enable"] and not source["video"]["QT"]["enable"]) and source["video"]["HD"]["enable"]:
        result["HD"] = encode.video(_transcoding_config["HD"])
        result["HD"]["mode"] = "ffmpeg"
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
        result["PNG"]["mode"] = "ffmpeg"
    else:
        result["PNG"] = created("PNG", "warning", created=False)

    return result
