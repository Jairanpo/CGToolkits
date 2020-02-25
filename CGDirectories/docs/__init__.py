import sys
import os


def select_correct_execution_path():
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
        print(datadir)
    else:
        datadir = os.path.dirname(__file__)
    return datadir


def get_sequence_documentation(document_name):
    document_path = os.path.join(select_correct_execution_path(), document_name)

    with open(document_path, "r") as file:
        return file.read()
