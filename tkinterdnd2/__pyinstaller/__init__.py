import os


def get_hook_dirs():
    """Entry point that lets PyInstaller find hook-tkinterdnd2.py automatically."""
    return [os.path.dirname(__file__)]
