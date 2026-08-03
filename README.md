# OverCoach

**OverCoach** is a free, open-source project designed to help players self-coach in Overwatch, The program also serves as an automated launcher for the game!

OverCoach is not a replacement for 1v1 coaching, but aims to help players self-coach in between proper coaching sessions (or even just to learn on their own).

**Python is required to run the application**

---

## Core Features

*   **Multi-Profile Management:** Create, delete, and switch between local student accounts with ease.
*   **Live Rank & Stat Syncing:** Programmatically pings OverFast API to pull PC or console ranks and most-played character averages.
*   **Zero-Configuration Game Launcher:** Launches Overwatch 2 natively via Steam or Battle.net(WIP) with a single click — no local file path configurations required!
*   **Dynamic Daily Challenges:** Automatically resets and rolls personalized, non-repeating gameplay focuses on startup.
*   **Learning Opportunities Database:** A built-in repository of gameplay layers and concepts to help increase your overall game knowledge.

---

## How to Run Locally

Since OverCoach is open-source, you can easily run and compile it on your own machine (compatible with Windows, macOS, and Linux):

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/DiamondEnderman/OverCoach-Challenges.git
    ```
2.  **Install Dependencies:**
    Make sure you have Python installed, then install the required GUI and network libraries:
    ```bash
    pip install flet requests
    ```
3.  **Download Your Local Assets:**
    Run the automated bulk downloader script to fetch your local Overwatch 2 hero portraits:
    ```bash
    python download_hero_icons.py
    ```
4.  **Launch the Application:**
    ```bash
    python app.py
    ```

---

## Legal Disclaimer

OverCoach is an unofficial, non-commercial fan-made companion application developed solely for community coaching and educational purposes. It is not associated with, authorized, sponsored, or endorsed by Blizzard Entertainment, Inc.

Overwatch and all associated names, logos, characters, and assets are registered trademarks of Blizzard Entertainment, Inc. All in-game screenshots, icons, and text descriptions are the property of their respective owners. No copyright or trademark infringement is intended.