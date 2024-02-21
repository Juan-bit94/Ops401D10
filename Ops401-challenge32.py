#!/usr/bin/env python3

# These are all the necessary modules
import os  # This module is for interacting with the operating system
import hashlib  # This module is for generating hash values
import time  # This module is for handling time-related operations

# This function generates a MD5 hash for a file
def generate_md5(file_path):
    # This will open the file in binary mode
    with open(file_path, "rb") as f:
        # This will read the file content in chunks to handle large files
        content = f.read()
        # This will alculate the MD5 hash of the file content
        md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash

# This function searches the for files and print relevant information
def search_files():
    # This prompts user for input
    file_name = input("Enter the file name to search for: ")
    search_directory = input("Enter the directory to search in: ")
    
    # This is a recursive function to scan each file and folder
    def scan_directory(directory):
        # This will iterate through each directory, subdirectory, and file within the given directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # This checks if the entered file name is contained in the file name
                if file_name.lower() in file.lower():
                    # This gets the file size
                    file_size = os.path.getsize(file_path)
                    # This gets a timestamp
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
                    # This generates a MD5 hash
                    md5_hash = generate_md5(file_path)
                    # This prints the information
                    print(f"Timestamp: {timestamp}, File Name: {file}, File Size: {file_size} bytes, File Path: {file_path}, MD5 Hash: {md5_hash}")
            for dir in dirs:
                # This recursive call scans subdirectories
                scan_directory(os.path.join(root, dir))
    
    # This calls the recursive function to start scanning
    scan_directory(search_directory)

if __name__ == "__main__":
    # Calling the search_files function
    search_files()
