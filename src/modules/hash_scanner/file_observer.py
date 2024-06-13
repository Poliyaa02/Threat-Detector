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

    #def is called after the creation of a new file in the specified folder
    def on_created(self, event):
        if not event.is_directory:      #Check if is a file and not a dir
            file_path = event.src_path  
            scan_result = self.hash_scanner.hash_scan(file_path)    #Scan the file using hash_scanner
            if "error" not in scan_result:
                is_malicious = self.hash_scanner.is_malicious(scan_result["popular_threat_categories"])     #Find if a file is malicious
                self.hash_scanner.logger.log_scan_result(is_malicious, file_path, scan_result["popular_threat_categories"], scan_result["type_description"])    #Log the scan results
            else:
                self.hash_scanner.logger.log_scan_result(False, file_path, ["Error"], scan_result["error"])
