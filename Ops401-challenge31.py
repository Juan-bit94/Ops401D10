# Script Name:					Ops401-challenge31.py
# Author: 					    Juan Maldonado
# Date of latest revision:		2/19/2024
# Purpose:					    This script is the bases for an antivirus tool for python. It will search files and directory, and if there is a positive
#                                detection, it will print to the screen the file name and location. Also at the end of the script, it will print how many files were searched and how many hits were found. 

#!/usr/bin/env python3

# This imports the os module to work with file paths and directories
import os  

# This imports a tabulate module to create tables for presentation purpose.
from tabulate import tabulate  

# This function searches based on user input. 
def search_files():
    # This prompts the user for file name to search for
    file_name = input("Enter the file name to search for: ")

    # This prompts the user for directory to search in
    search_directory = input("Enter the directory to search in: ")

    # This initializes the counters for files searched and hits found
    files_searched = 0
    hits_found = 0

    # This searches for files in the specified directory
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if file_name.lower() in file.lower():  # This checks if the file name contains the search string
                hits_found += 1
                file_path = os.path.join(root, file)  # This gets the full path of the file
                print(f"Found: {file} at {file_path}")  # This prints the file name and its location
            files_searched += 1  # This increments the counter for files searched

    # This creates a table for the summary portion of the code
    summary_table = [["Files Searched", files_searched], [ "Hits Found", hits_found]]
    
    # This prints the summary as a table
    print(f"\nSearch completed.")
    print(tabulate(summary_table, headers=["Metric", "Value"], tablefmt="grid"))

if __name__ == "__main__":
    search_files()  # This calls the search_files function when the script is executed
