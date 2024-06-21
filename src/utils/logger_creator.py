import os
import datetime
import socket
import logging

'''
The LoggerCreator class manages logging, writing the results in a local file.
'''


class LoggerCreator:
    def __init__(self):
        self.log_file_path = os.path.join("src", "data", "local_log")
        self.setup_logging()


    def setup_logging(self):
        try:
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

            self.logger = logging.getLogger('hash_scanner')
            self.logger.setLevel(logging.DEBUG)
            
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(logging.DEBUG)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        except OSError as e:
            print(f"Error: Failed to create log directory or file: {e}")
            raise

    def log_scan_result(self, is_malicious, file_name):
        try:
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            ip_address = self.get_private_ip()
            severity = "Malicious" if is_malicious else "Safe"
            hostname = socket.gethostname()
            
            log_entry = f"{timestamp} - {ip_address} - {severity} - {hostname} - {file_name}"
            self.logger.info(log_entry)
        except Exception as e:
            self.logger.error(f"Failed to log scan result: {e}")

    def get_private_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            s.connect(('10.254.254.254', 1))
            ip_address = s.getsockname()[0]
        except socket.error as se:
            self.logger.error(f"Socket error: {se}")
            ip_address = '127.0.0.1'
        except Exception as e:
            self.logger.error(f"Failed to retrieve private IP: {e}")
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address