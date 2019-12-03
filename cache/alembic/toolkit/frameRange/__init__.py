def validate(start, end):
    result = {
        "status": False,
        "message": "Invalid"
    }
    if start > end:
        result["message"] = "You didn't provide a valid range."
        return result

    result["status"] = True
    result["message"] = "Valid range."

    return result
