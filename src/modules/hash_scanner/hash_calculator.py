import hashlib

'''
This script defines HashCalculator class, which calculates SHA-256 hashes for the files.
'''

class HashCalculator:
    def __init__(self):
        pass

    def calculate_hashes(self, file_paths):
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        hash_dict = {}
        for file_path in file_paths:
            try:
                hasher = hashlib.sha256()
                with open(file_path, "rb") as f:
                    while True:
                        data = f.read(65536)
                        if not data:
                            break
                        hasher.update(data)
                hash_value = hasher.hexdigest()
                return file_path, hash_value
            except Exception as e:
                print(f"Error calculating hash for file {file_path}: {e}")
                return file_path, None