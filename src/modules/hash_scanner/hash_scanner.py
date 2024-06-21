import yaml
import requests
import json

'''
This script defines a HashScanner class which scans files hashes for potential threats using the VirusTotal API.
The class reads configuration settings from a YAML file, calculates file hashes, sends requests to the VirusTotal
API, interprets the response, and determines if a file is malicious.
Scan results are logged using a provided logger.
'''

class HashScanner:
    def __init__(self, logger, hash_calculator):
        with open("src/data/config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.api_key_value = config["API_KEY"]
        self.key_name = config["KEY_NAME"]
        self.logger = logger
        self.hash_calculator = hash_calculator
    
    def is_malicious(self, threat_category):
        # Check if the list of threat_category is empty, and return a Bool based on the result
        return len(threat_category) > 0
    
    def hash_scan(self, file_path):
        # Calculate the hash of the file
        _, file_hash = self.hash_calculator.calculate_hashes(file_path)
        if not file_hash:
            return {"error": "Failed to calculate hash"}
        
        # Request URL for the VirusTotal API
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_key_value
        }

        # Send the GET request to the VirusTotal API
        response = requests.get(url, headers=headers)
        
        # Process the API response
        if response.status_code == 200:
            data = json.loads(response.text)
            attributes = data.get('data', {}).get('attributes', {})
            
            if attributes:
                # Extract the relevant information from the JSON response
                names = attributes.get('names', [])
                reputation = attributes.get('reputation', 0)
                
                popular_threat_categories = attributes.get('popular_threat_classification', {}).get('popular_threat_category', [])
                popular_threat_names = attributes.get('popular_threat_classification', {}).get('popular_threat_name', [])
                suggested_threat_label = attributes.get('popular_threat_classification', {}).get('suggested_threat_label', "")
                
                tags = attributes.get('tags', [])
                type_description = attributes.get('type_description', "")
                
                # Construct the result Dictionary
                result = {
                    "names": names,
                    "reputation": reputation,
                    "popular_threat_categories": [category['value'] for category in popular_threat_categories],
                    "popular_threat_names": [name['value'] for name in popular_threat_names],
                    "suggested_threat_label": suggested_threat_label,
                    "tags": tags,
                    "type_description": type_description,
                }

                # Log the result
                is_malicious = self.is_malicious(result["popular_threat_categories"])
                self.logger.log_scan_result(is_malicious, file_path)
                
                return result
            else:
                return {"error": "No attributes found"}
        else:
            # Return an error message based on the response HTTP code, if the response was not 200
            return {"error": f"Error: {response.status_code}"}
