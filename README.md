# Threat-Detector

Threat-Detector is a software based on the "Pyramid of Pain" theoretical cybersecurity model. This software monitors every action, scans it, and logs it in an easy-to-understand manner. It is easy to set up and utilizes cloud scanning, based on VirusTotal, ensure activities are checked using the most recent malware database, guaranteeing up-to-date scanning.

## Installation

1. Open Terminal

2. Clone the Github Repository:
    `git clone https://github.com/Poliyaa02/Threat-Detector`

3. Navigate to the Directory
    `cd Threat-Detector`

4. Install Dependencies
    `pip install -r requirements.txt`

5. Run the software


## Usage 

> [!IMPORTANT]
>  This initial version just scans file hashes to determine whether they are a malware or not.

# Running with Config file
First configure the **config.yaml** file, specify the folder to scan and your VirusTotal API key. Then, execute the software from the terminal using `python threatdetector.py`,

# Running with Command-line Arguments
First configure the **config.yaml** file, specify your VirusTotal API key. Then, execute the software from the terminal using `python threatdetector.py -p /path/to/scan` specify the folder to scan after the "-p" flag


The software will monitor the specified folder for new events. Upon detecting a new file, it automatically calculates its hash and performs an online scan to identify if it's a malicious file. The results are displayed on-screen and logged in the **local_log** file.

[^1] What is the [pyramid of pain](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)?