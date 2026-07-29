import sys
import traceback as tb
import datetime as dt
import libraries.controllers.file_controller as fc
import os
import libraries.consts as consts

LOG_FOLDER_PATH = fc.SYSTEM_PATHS["logs"]

def log_exception(exc_type, exc_value, exc_traceback) -> None:
    timestamp = dt.now().strftime("%Y-%m-%d_%H:%M:%S")

    log_path = os.path.join(LOG_FOLDER_PATH, f"{timestamp}.log")

    traceback_lines = tb.format_exception(exc_type, exc_value, exc_traceback)
    formatted_traceback = "".join(traceback_lines)

    log_entry = (
        f"====================================\n"
        f"CRASH TIMESTAMP: {timestamp}\n"
        f"APP VERSION: {consts.VERSION_NUMBER}\n"
        f"====================================\n"
        f"{formatted_traceback}\n"
    )

    fc.initialize_system_folders()
    with open(log_path, "a") as file:
        file.write(log_entry)

    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def initialize_crash_logger() -> None:
    sys.excepthook = log_exception