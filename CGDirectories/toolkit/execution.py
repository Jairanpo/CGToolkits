import os
import sys


def setup():
    if getattr(sys, 'frozen', False):
        # print(os.path.dirname(sys.executable))
        pass
    else:
        path = os.path.abspath(os.getcwd())
        if path not in sys.path:
            sys.path.append(path)
        else:
            pass
