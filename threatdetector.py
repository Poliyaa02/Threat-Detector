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
    # Get the current username
    username = getpass.getuser()
    config_path = os.path.join(os.path.dirname(__file__), "data", "config.yaml")
    config_path = config_path.replace("{username}", username)

    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
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
            scan_folder = args.file_path
        else:
            config = load_config()
            scan_folder = config.get("SCAN_FOLDER")

        if not scan_folder or not os.path.exists(scan_folder):
            raise ValueError(f"SCAN_FOLDER '{scan_folder}' specified in config.yaml does not exist or is not valid.")

        print(f"scanning folder: {scan_folder}")
        # Initialize HashCalculator
        hash_calculator = HashCalculator()

        # Initialize LoggerCreator
        logger = Logger()

        # Initialize HashScanner
        hash_scanner = HashScanner(logger, hash_calculator)

        # Initialize FileObserver 
        observer = Observer()
        observer.schedule(FileObserver(hash_scanner), scan_folder, recursive=True)
        observer.start()
        print(f"Observer started on folder: {scan_folder}")

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
