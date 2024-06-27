import os
import datetime

'''
The LoggerCreator class manages logging, writing the results in a local file.
'''

class Logger:
    def __init__(self):
        self.log_file_path = "data/local_log"

        try:
            self.log_file = open(self.log_file_path, "a")  # Open log file in append mode
        except IOError as e:
            print(f"Failed to open log file: {e}")

    def log_scan_result(self, is_malicious, file_name, threat_category, type_description):
        try:
            timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            user = self.get_current_user()
            threat_label = "Malicious" if is_malicious else "Safe"
            threat_category_text = ", ".join(threat_category) if threat_category else "Safe"
            short_file_name = os.path.basename(file_name)
            log_entry = f"[{timestamp}] [{user}] [{threat_label}] - {short_file_name} - {threat_category_text} - {type_description}\n"
            try:
                self.log_file.write(log_entry)
                self.log_file.flush()
            except Exception as e:
                print(f"Failed to write log: {e}")

            print(log_entry)
        except Exception as e:
            print(f"Failed to log scan result: {e}")

    def __del__(self):
        try:
            self.log_file.close()
        except AttributeError:
            pass

    def get_current_user(self):
        try:
            return os.getlogin()
        except Exception:
            try:
                import pwd
                return pwd.getpwuid(os.getuid()).pw_name
            except Exception as e:
                print(f"Failed to get current user: {e}")
                return "unknown_user"
