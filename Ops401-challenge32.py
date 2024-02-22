# Script Name:					Ops401-challenge33.py
# Author: 					    Juan Maldonado
# Date of latest revision:		2/21/2024
# Purpose:					    script builds upon the last one (Ops401-challenge32.py). Now it connects to an API, compares hashes, and prints a report to the screen.

#!/usr/bin/env python3

import os  # This is for interacting with the OS
import hashlib  # This allows for the generation the hash values
import time  # This is for handling time-related operations
import requests  # This is for making HTTP requests to the an API

# This gets the API key from the environment variables
# If you get an error, that means you have to make an envitonmental variable on the command line
# try making it a global one
API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

# This function generates an MD5 hash for a file
def generate_md5(file_path):
    # This opens the file in binary mode
    with open(file_path, "rb") as f:
        # This reads the content of the file
        content = f.read()
        # This calculates the MD5 hash based on file content
        md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash

# This function searches for files and check them against VirusTotal
def search_files():
    # This prompts the user for input
    file_name = input("Please enter the file name to search for: ")
    search_directory = input("Please enter the directory to search in: ")
    
    # This is the recursive function to scan the directory and its subdirectories
    def scan_directory(directory):
        # This iterates through each directory, subdirectory, and file within the given directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # This checks if the entered file name is contained in the file name
                if file_name.lower() in file.lower():
                    file_size = os.path.getsize(file_path)
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
                    md5_hash = generate_md5(file_path)
                    # This prints some file information
                    print(f"File Name: {file}, File Size: {file_size} bytes, File Path: {file_path}, Timestamp: {timestamp}, MD5 Hash: {md5_hash}")
                    # This checks file hash against VirusTotal
                    check_file_with_vt(md5_hash)
                    
            for dir in dirs:
                # This is the recursive call to scan subdirectories
                scan_directory(os.path.join(root, dir))
    
    # This calls the recursive function to start scanning
    scan_directory(search_directory)

# This function checks a file hash against VirusTotal
def check_file_with_vt(md5_hash):
    # This constructs the URL for querying VirusTotal API
    url = f"https://www.virustotal.com/api/v3/files/{md5_hash}"
    headers = {
        'x-apikey': API_KEY
    }
    # This makes a GET request to VirusTotal API
    response = requests.get(url, headers=headers)
    
    # This checks the response status code
    if response.status_code == 200:
        # This parses the JSON response
        json_response = response.json()
        data = json_response['data']
        if 'attributes' in data:
            attributes = data['attributes']
            # This gets the number of positives and total scans
            total_positives = attributes['last_analysis_stats']['malicious'] + attributes['last_analysis_stats']['suspicious']
            total_scans = attributes['last_analysis_stats']['harmless'] + total_positives
            # This prints results
            print(f"Positives: {total_positives}, Total Scans: {total_scans}")
        else:
            print("File not found on VirusTotal.")
    else:
        print("Error occurred while querying VirusTotal API.")

# Main block
if __name__ == "__main__":
    # Call the search_files function
    search_files()
