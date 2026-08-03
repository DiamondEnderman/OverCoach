import requests
import os
import warnings

import libraries.controllers.file_controller as file_controller

#WILL NEED TO MOVE AROUND FILES IN THE GITHUB REPO, THIS WILL BREAK THE PREVIOUS VERSION\
_REPO_REGISTRY = { #in  name: github name
    "challenges": "OverCoach-Challenges",
    "learning_db": "OverCoach-Learning-Database"
}

class _FilesToSync:
    CHALLENGES = [        
        "layer1.json",
        "layer2.json",
        "layer3.json",
        "layer4.json"
    ]
    LEARNING_DB = [
        "beginner.json"
    ]

class Git:
    def __init__(self, repo_key: str):
        if repo_key not in _REPO_REGISTRY:
            raise ValueError(
                f"Invalid repo_key: '{repo_key}'. "
                f"Expected one of the following: {list(_REPO_REGISTRY.keys())}"
            )
        
        self.local_path = file_controller.SYSTEM_PATHS.get(repo_key)
        self.repo_name = _REPO_REGISTRY.get(repo_key)

        self.base_url = f"https://raw.githubusercontent.com/DiamondEnderman/{self.repo_name}/refs/heads/main/"
        self.version_url = f"{self.base_url}version.json"

        self.files_to_sync = getattr(_FilesToSync, repo_key.upper(), None)

    def get_local_version(self):
        json_path = os.path.join(self.local_path, "version.json")
        if not os.path.exists(json_path):
            return "0.0.0"
        return file_controller.pull_data(json_path).get("version_number", "0.0.0")

    def get_latest_version(self):
        print(f"Attempting to get the latest version number from github.\nRepo: {self.repo_name}")
        response = requests.get(self.version_url, timeout = 10)
        response.raise_for_status()
        return response.json().get("version_number", None)

    def _download_data(self, latest_version_number):
        for file in self.files_to_sync:
            url = f"{self.base_url}{file}"
            print(f"Downloading '{file}' from {url}")
            response = requests.get(url, timeout = 10)
            response.raise_for_status()

            file_path = os.path.join(self.local_path, file)
            file_controller.push_data(file_path, response.json())

        version_path = os.path.join(self.local_path, "version.json")
        version_data = {
            "version_number": latest_version_number
        }
        file_controller.push_data(version_path, version_data)

        print("Downloads Complete!")

    def sync(self):
        print(f"Syncing Files for Repo: {self.repo_name}")
        try:
            local_version = self.get_local_version()
            latest_version = self.get_latest_version()

            if local_version != latest_version:
                self._download_data(latest_version)
            else:
                print("Files Up to Date!")
        except requests.exceptions.RequestException as err:
            print(f"Offline or couldnt reach GitHub repo ({err}). \n Loading local data.")

        except Exception as err:
            print(f"An unexpected error occured: {err}")



def sync_all():
    for repo in _REPO_REGISTRY.keys():
        Git(repo).sync()