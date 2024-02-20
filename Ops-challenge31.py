# Script Name:					Ops-challenge31.py
# Author: 					    Juan Maldonado
# Date of latest revision:		2/19/2024
# Purpose:					    Tis script is the bases for an antivirus tool for python. It will search files and directory, and if there is a positive
#                       detection, it will print to the scren the file name and location.

#!/usr/bin/env python3

import os  # Import the os module to work with file paths and directories

def search_files():
    # Prompt user for file name to search for
    file_name = input("Enter the file name to search for: ")

    # Prompt user for directory to search in
    search_directory = input("Enter the directory to search in: ")

    # Initialize counters for files searched and hits found
    files_searched = 0
    hits_found = 0

    # Search for files in the specified directory
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if file_name.lower() in file.lower():  # Check if the file name contains the search string
                hits_found += 1
                file_path = os.path.join(root, file)  # Get the full path of the file
                print(f"Found: {file} at {file_path}")  # Print the file name and its location
            files_searched += 1  # Increment the counter for files searched

    # Print summary
    print(f"\nSearch completed.")
    print(f"Files searched: {files_searched}")
    print(f"Hits found: {hits_found}")

if __name__ == "__main__":
    search_files()  # Call the search_files function when the script is executed
