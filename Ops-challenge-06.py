# Script Name:					File Encryption Script part 1
# Author: 					    Juan Maldonado
# Date of latest revision:		1/16/2024
# Purpose:					    This script encrypts a single file. 

# This imports necessary modules for cryptography 
# I got information about this module at this site: https://thepythoncode.com/article/encrypt-decrypt-files-symmetric-python
from cryptography.fernet import Fernet
import os

# This function generates a key for encryption/decryption 
def generate_key():
    return Fernet.generate_key() # This line of code generates a key using Fernet

# This function encrypts a file using the generated key.
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file: # This opens a file in binary mode
        data =file.read() # This reads the file content
    cipher_suite = Fernet(key) # This creates a Fernet cipher suite with the provided key
    encrpted_data = cipher_suite.encrypt(data) # This encrypts the file content
    with open(file_path, 'wb') as file: # This opens the file in binary mode for writing
        file.write(encrpted_data) # This writes the encrypted content back to the file. 

# This function decrypts a file using the generated key
def decrypt_file(file_path, key): 
    with open(file_path, 'rb') as file: 
        data = file.read()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data) # This decrypts the file content
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

# This function encrypts a string using the generated key
def encrypt_string(plaintext, key):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(plaintext.encode())
    print("Encrypted String:", encrypted_text.decode())

# This function decrypts a string using the generated key
def decrypt_string(ciphertext, key):
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(ciphertext.encode())
    print("Decrypted String:", decrypted_text.encode())

def main():
    # This generates a key for encryption/decryption
    # It also calls the generate_key function and stores the key here
    key = generate_key()
    
    # This starts a loop for the user to keep using the script untill they want to leave the script.
    while True:
        print("Welcome to the File encryption tool!") 
        print("Please select the following options: ")   
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Encrypt a message")
        print("4. Decrypt a message")
        print("q. to quit the script")

        # This prompts the user to make a choice
        user_selction = input("Enter a number to make a selction or q to quit: ")

        # This checks if the user wants to quit
        if user_selction.lower() == 'q':
            break 
        
        try:

            # This convert user input to integer
            user_selction = int(user_selction)

            # This executes certain functions depending on user choice
            if user_selction in [1, 2]:
                file_path = input("Please enter the file path to begin encryption:")
                if user_selction == 1:
                    encrypt_file(file_path, key)
                    print("File encrypted successfully.")
                elif user_selction == 2:
                    decrypt_file(file_path, key)
                    print("File decrypted successfully.")
            elif user_selction in [3,4]: 
                message = input("Please enter a message to encrypt: ")
                if user_selction == 3:
                    encrypt_string(message, key)
                elif user_selction == 4:
                    decrypt_string(message, key)
            else:
                print("I am sorry but the input was invalid. Please enter a number between 1 and 4, or q to leave.")
        except ValueError:
            print("Sorry, the value you entered is invalid, please enter a number between 1 and 4 or quit to leave.")

if __name__ == "_main__":
    main()

