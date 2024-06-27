from watchdog.events import FileSystemEventHandler

'''
This code defines a class called FileObserver, the class inherits from FileSystemEventHandler. 
It monitors the folder specified in the config.yaml for newly created files and uses hash_scanner to calculate 
the hash of the new files and scan them for potential threats using VirusTotal API. The results of the scan are 
logged using a logger.
'''


class FileObserver(FileSystemEventHandler):
    def __init__(self, hash_scanner):
        super().__init__()
        self.hash_scanner = hash_scanner

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"New file created: {file_path}")
            self.process_new_file(file_path)

    def process_new_file(self, file_path):
        try:
            is_malicious = self.hash_scanner.hash_scan(file_path)
            self.hash_scanner.logger.log_scan_result(is_malicious, file_path)
        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")
