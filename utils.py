import os
import sys


def resource_path(relative_path):
    # if getattr(sys, 'frozen', False):
    #     EXE_LOCATION = os.path.dirname( sys.executable ) # frozen
    # else:
    #     EXE_LOCATION = os.path.dirname( os.path.realpath( __file__ ) ) # unfrozen
    # return os.path.join( EXE_LOCATION, relative_path)
    # # """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)