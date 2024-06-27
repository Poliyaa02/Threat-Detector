import os
import getpass
import yaml
from watchdog.observers import Observer
from modules.hash_scanner.hash_calculator import HashCalculator
from modules.hash_scanner.hash_scanner import HashScanner
from modules.hash_scanner.file_observer import FileObserver
from lib.logger import Logger
from lib.cli import CommandInterface

def load_config():
    username = getpass.getuser()
    config_path = os.path.join(os.path.dirname(__file__), "data", "config.yaml")

    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config_content = config_file.read()
            config_content = config_content.format(username=username)  # Perform substitution
            config = yaml.safe_load(config_content)
            return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error with the YAML file '{config_path}': {e}")
        return {}

def main():
    try:
        print("Parsing command line arguments...")
        args = CommandInterface.parse_arguments()
        print(f"Arguments parsed: {args}")

        if args.file_path:
            scan_folders = [args.file_path]
        else:
            config = load_config()
            scan_folders = config.get("SCAN_FOLDER", [])

        if not scan_folders:
            raise ValueError("No valid SCAN_FOLDER specified in config.yaml.")

        for scan_folder in scan_folders:
            if not os.path.exists(scan_folder):
                raise ValueError(f"SCAN_FOLDER '{scan_folder}' specified in config.yaml does not exist or is not valid.")

        print(f"Scanning folders: {scan_folders}")

        # Initialize HashCalculator
        hash_calculator = HashCalculator()

        # Initialize LoggerCreator
        logger = Logger()

        # Initialize HashScanner
        hash_scanner = HashScanner(logger, hash_calculator)

        # Initialize FileObserver
        observer = Observer()
        for scan_folder in scan_folders:
            observer.schedule(FileObserver(hash_scanner), scan_folder, recursive=True)
            print(f"Observer started on folder: {scan_folder}")
        observer.start()

        try:
            while True:
                pass

        except KeyboardInterrupt:
            print("KeyboardInterrupt received, stopping observer...")
            observer.stop()
            observer.join()
            print("Observer stopped.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()