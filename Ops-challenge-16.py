# Script Name:					Ops-challenge-16.py
# Author: 					    Juan Maldonado
# Date of latest revision:		1/29/2024
# Purpose:					    This is a custom tool that performs brute force attacks to better unsetstand
#                       the types of automation employed by adversaries. 

import time

# This function is for Mode 1: Offensive; Dictionary Iterator
def iterator():
    # This prompts the user to input the word list file path
    filepath = input("Enter your word list file path:\n")

    try:
        # This opens the specified word list file and it handles potential encoding issues
        with open(filepath, encoding="ISO-8859-1") as file:
            # This iterates through each line in the file
            for line in file:
                word = line.strip()  # This removes the leading and trailing whitespaces from the word
                print("Current Word:", word)  
                time.sleep(1)  # This adds a delay of 1 second between words to simulate iteration
    except FileNotFoundError:
        print(f"File not found at path: {filepath}")  # This prints an error message if the file is not found
    except Exception as e:
        print(f"An error occurred: {e}")  # This prints a generic error message if an exception occurs

# This function is for Mode 2: Defensive; Password Recognized
def checks_password():
    # This prompts the user to input the string to search for and the word list file path
    user_string = input("Please enter a word to search for:\n")
    filepath = input("Please enter your word list file path:\n")

    try:
        # This opens the specified word list file and again handles potential encoding issues
        with open(filepath, encoding="ISO-8859-1") as file:
            # This creates a list of words from the file using list comprehension
            word_list = [line.strip() for line in file]

        # This checks if the user input string is in the word list
        if user_string in word_list:
            print(f"The word '{user_string}' appeared in the list.")
        else:
            print(f"The input '{user_string}' did not appear in the list.")
    except FileNotFoundError:
        print(f"Looks like the file was not found at path: {filepath}")  # Print an error message if the file is not found
    except Exception as e:
        print(f"An error occurred: {e}")  # Print a generic error message if an exception occurs

# Main block
if __name__ == "__main__":
    while True:
        # This displays the menu to the user and prompt for input
        mode = input("""
Brute Force Wordlist Attack Tool Menu
1 - Offensive; Dictionary Iterator
2 - Defensive; Password Recognized
3 - Exit
    Please enter a number: 
""")
        if mode == "1":
            iterator()  # This calls the iterator function for Mode 1
        elif mode == "2":
            checks_password()  # This calls the check_password function for Mode 2
        elif mode == '3':
            break  # This exits the script for Mode 3
        else:
            print("Invalid selection...")  # This displays an error message for invalid input
