import os
import yaml
from watchdog.observers import Observer
from src.modules.hash_scanner.hash_calculator import HashCalculator
from src.modules.hash_scanner.hash_scanner import HashScanner
from src.modules.hash_scanner.file_observer import FileObserver
from src.utils.logger_creator import LoggerCreator
from src.utils.command_interface import CommandInterface

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "src", "data", "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{config_path}': {e}")
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
        # Initialize HashCalculator instance
        hash_calculator = HashCalculator()

        # Initialize LoggerCreator instance
        logger = LoggerCreator()

        # Initialize HashScanner instance with LoggerCreator for logging
        hash_scanner = HashScanner(logger, hash_calculator)

        # Initialize FileObserver with HashScanner instance
        observer = Observer()
        observer.schedule(FileObserver(hash_scanner), scan_folder, recursive=True)
        observer.start()
        print(f"Observer started on folder: {scan_folder}")

        try:
            while True:
                pass  # Keep the program running to handle events

        except KeyboardInterrupt:
            print("KeyboardInterrupt received, stopping observer...")
            observer.stop()
            observer.join()
            print("Observer stopped.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
