import sys
import os


path = os.path.abspath(os.getcwd())

print(path)

if not path in sys.path:
    sys.path.append(path)
