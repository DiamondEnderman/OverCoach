import libraries.controllers.file_controller as filecontroller
from libraries.consts import AppConfig
import os

SETTINGS_PATH = filecontroller.SYSTEM_PATHS["settings"]

CONFIG_FILE_PATH = os.path.join(SETTINGS_PATH, AppConfig.CONFIG_FILE_NAME)

class _Config:
    def __init__(self):
        self._initialize()

        if self.get("launcher") is None:
            self.set("launcher", "steam")

    def _initialize(self):
        if not os.path.exists(CONFIG_FILE_PATH):
            filecontroller.push_data(CONFIG_FILE_PATH, {})
        self.load_from_file()

    def save_to_file(self) -> None:
        filecontroller.push_data(CONFIG_FILE_PATH, self.config)

    def load_from_file(self) -> dict:
        self.config = filecontroller.pull_data(CONFIG_FILE_PATH)

        return self.config
    
    def set(self, setting, value) -> None:
        self.config[setting] = value
        self.save_to_file()

    def get(self, setting):
        return self.config.get(setting, None)
    
CONFIG = _Config()