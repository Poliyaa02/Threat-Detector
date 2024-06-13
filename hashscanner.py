import os
import yaml
from watchdog.observers import Observer
from src.modules.hash_scanner.file_observer import FileObserver
from src.modules.hash_scanner.hash_calculator import HashCalculator
from src.modules.hash_scanner.hash_scanner import HashScanner
from src.modules.hash_scanner.logger_creator import LoggerCreator

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "src", "data", "config.yaml")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def main():
    config = load_config()

    hash_calculator = HashCalculator()
    logger = LoggerCreator()  # Ensure LoggerCreator initializes correctly

    hash_scanner = HashScanner(logger, hash_calculator)

    observer = Observer()
    observer.schedule(FileObserver(hash_scanner), config["SCAN_FOLDER"], recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
