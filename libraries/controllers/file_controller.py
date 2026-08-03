import os
import json
import shutil

IS_TEST = True

_APPDATA = os.getenv("APPDATA")

if _APPDATA is None:
    _APPDATA = os.path.expanduser("~/.config")

_master_folder_names = {
    "live": "OverCoach",
    "test": "OverCoachTest"
}

_state = "test" if IS_TEST else "live"

_MASTER_PATH = os.path.join(_APPDATA, _master_folder_names[_state])

_REQUIRED_FOLDERS = [
    "settings",
    "profiles",
    "cache",
    "logs",
    "challenges",
    "learning_db"
]

SYSTEM_PATHS = {
    name: os.path.join(_MASTER_PATH, name)
    for name in _REQUIRED_FOLDERS
}

def initialize_system_folders():
    if not os.path.exists(_MASTER_PATH):
        os.makedirs(_MASTER_PATH)
        print("Appdata folder not found, creating a new one")

    for name, path in SYSTEM_PATHS.items():
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"{name} folder not found, creating a new one")


def get_folder_path(parent: str, name: str):
    return os.path.join(SYSTEM_PATHS[parent], name)

def create_folder(parent: str, name: str):
    path = get_folder_path(parent, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def remove_folder(parent: str, name: str):
    path = get_folder_path(parent, name)
    if os.path.exists(path):
        shutil.rmtree(path)

def push_data(file_path:str, data):
    parent_dir = os.path.dirname(file_path)

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)

def pull_data(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)