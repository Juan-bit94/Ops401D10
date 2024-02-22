#!/usr/bin/env python3

# Import necessary modules
import os  # For interacting with the operating system
import hashlib  # For generating hash values
import time  # For handling time-related operations
import requests  # For making HTTP requests to the VirusTotal API

# VirusTotal API key - Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'

# Function to generate MD5 hash for a file
def generate_md5(file_path):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the content of the file
        content = f.read()
        # Calculate the MD5 hash of the file content
        md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash

# Function to search for files and check them against VirusTotal
def search_files():
    # Prompt the user for input
    file_name = input("Enter the file name to search for: ")
    search_directory = input("Enter the directory to search in: ")
    
    # Recursive function to scan the directory and its subdirectories
    def scan_directory(directory):
        # Iterate through each directory, subdirectory, and file within the given directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Check if the entered file name is contained in the file name
                if file_name.lower() in file.lower():
                    file_size = os.path.getsize(file_path)
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
                    md5_hash = generate_md5(file_path)
                    # Print file information
                    print(f"File Name: {file}, File Size: {file_size} bytes, File Path: {file_path}, Timestamp: {timestamp}, MD5 Hash: {md5_hash}")
                    # Check file hash against VirusTotal
                    check_file_with_vt(md5_hash)
                    
            for dir in dirs:
                # Recursive call to scan subdirectories
                scan_directory(os.path.join(root, dir))
    
    # Call the recursive function to start scanning
    scan_directory(search_directory)

# Function to check a file hash against VirusTotal
def check_file_with_vt(md5_hash):
    # Construct the URL for querying VirusTotal API
    url = f"https://www.virustotal.com/api/v3/files/{md5_hash}"
    headers = {
        'x-apikey': API_KEY
    }
    # Make a GET request to VirusTotal API
    response = requests.get(url, headers=headers)
    
    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        data = json_response['data']
        if 'attributes' in data:
            attributes = data['attributes']
            # Get the number of positives and total scans
            total_positives = attributes['last_analysis_stats']['malicious'] + attributes['last_analysis_stats']['suspicious']
            total_scans = attributes['last_analysis_stats']['harmless'] + total_positives
            # Print the results
            print(f"Positives: {total_positives}, Total Scans: {total_scans}")
        else:
            print("File not found on VirusTotal.")
    else:
        print("Error occurred while querying VirusTotal API.")

# Main block
if __name__ == "__main__":
    # Call the search_files function
    search_files()
