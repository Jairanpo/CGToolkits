import os
import sys
import win32com.client


def select_correct_execution_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)


def add_link(source, destination, name):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(source, name))
    shortcut.Targetpath = destination
    shortcut.WindowStyle = 1
    shortcut.save()


if __name__ == "__main__":
    state = True

    while state:
        print(len(sys.argv))

        try:
            add_link(sys.argv[2], sys.argv[3], sys.argv[4])
        except:
            print("Unable to create your link")

        user_input = input("Type \"exit\" to end the program: ")
        if user_input == "exit":
            state = False
