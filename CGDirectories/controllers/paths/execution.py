import os
import sys
import re


def root():
    pattern = re.compile('controllers.*')
    if getattr(sys, 'frozen', False):
        result = os.path.dirname(sys.executable)
        result = re.sub(pattern, "", result)
    else:
        result = os.path.dirname(__file__)
        result = re.sub(pattern, "", result)
    return result
