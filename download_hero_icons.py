import os
import requests
from typing import List

"""
This code is written by AI, I was too lazy too download all of the
hero icons and I didnt want to write a script for it myself.

however this might be cleaned up and remain in the finished product
since it could be useful for troubleshooting
"""

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIRECTORY = os.path.join(SCRIPT_DIR, "assets", "heroes")

# --- Domain 1: Directory Setup ---
def _ensure_directory_exists(path: str) -> None:
    """Creates the target directory if it does not exist on the disk."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


# --- Domain 2: API Client ---
def _fetch_hero_list() -> List[dict]:
    """Pings the OverFast API to retrieve the list of all Overwatch 2 heroes."""
    url = "https://overfast-api.tekrop.fr/heroes"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


# --- Domain 3: File Downloader ---
def _download_image(url: str, save_path: str) -> None:
    """Downloads a binary image from a URL and saves it directly to disk.
    
    Uses stream=True to handle downloading binary files safely in chunks
    without overloading the computer's memory.
    """
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()
    
    with open(save_path, "wb") as file:
        # Read the file in 8KB chunks to keep memory usage low
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)


# --- Domain 4: Main Coordinator ---
def main() -> None:
    """Coordinates the bulk download process."""
    print("Starting bulk download of Overwatch 2 hero portraits...")
    
    # Ensure our local assets folder is ready
    _ensure_directory_exists(OUTPUT_DIRECTORY)
    
    try:
        # Grab the list of heroes from the API
        heroes = _fetch_hero_list()
        print(f"Found {len(heroes)} heroes. Beginning download...\n")
        
        # Loop through and download each one
        for index, hero in enumerate(heroes, start=1):
            key = hero.get("key")
            portrait_url = hero.get("portrait")
            
            if not key or not portrait_url:
                continue
            
            # Construct the local filename (e.g., "assets/heroes/wrecking-ball.png")
            filename = f"{key}.png"
            save_path = os.path.join(OUTPUT_DIRECTORY, filename)
            
            print(f"[{index}/{len(heroes)}] Downloading {key.title()} -> {filename}...")
            _download_image(portrait_url, save_path)
            
        print("\nAll hero portraits successfully downloaded and saved locally!")
        
    except requests.exceptions.RequestException as err:
        print(f"\nNetwork Error occurred: {err}")
    except Exception as err:
        print(f"\nAn unexpected error occurred: {err}")


if __name__ == "__main__":
    main()