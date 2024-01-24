from cryptography.fernet import Fernet


# This function generates a key for encryption/decryption 
def generate_key():
    return Fernet.generate_key()


# This function encrypts a file using the generated key.
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)


# This function decrypts a file using the generated key
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data)
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
    print("Decrypted String:", decrypted_text.decode())


# This function recursively encrypts all files in a folder and child-folder
def encrypt_folder(folder_path, key):
    for folder_name, child_folders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            encrypt_file(file_path, key)


# This function recursively decrypts all files in a folder and its child-folders
def decrypt_folder(folder_path, key):
    for folder_name, child_folders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            decrypt_file(file_path, key)


def main():
    key = generate_key()

    while True:
        print("Welcome to the File encryption tool!")
        print("Please select the following options: ")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Encrypt a message")
        print("4. Decrypt a message")
        print("5. Recursively encrypt a folder")
        print("6. Recursively decrypt a folder")
        print("q. to quit the script")

        user_choice = input("Enter a number to make a selection or q to quit: ")

        if user_choice.lower() == 'q':
            break

        try:
            user_choice = int(user_choice)

            if user_choice in [1, 2]:
                file_path = input("Please enter the file path to begin encryption/decryption:")
                if user_choice == 1:
                    encrypt_file(file_path, key)
                    print("File encrypted successfully.")
                elif user_choice== 2:
                    decrypt_file(file_path, key)
                    print("File decrypted successfully.")
            elif user_choice in [3, 4]:
                message = input("Please enter a message to encrypt/decrypt: ")
                if user_choice == 3:
                    encrypt_string(message, key)
                elif user_choice == 4:
                    decrypt_string(message, key)
            elif user_choice == 5:
                folder_path = input("Please enter the folder path to recursively encrypt:")
                encrypt_folder(folder_path, key)
                print("Folder encrypted successfully.")
            elif user_choice == 6:
                folder_path = input("Please enter the folder path to recursively decrypt:")
                decrypt_folder(folder_path, key)
                print("Folder decrypted successfully.")
            else:
                print("Invalid input. Please enter a number between 1 and 6, or q to leave.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6, or q to leave.")


if __name__ == "__main__":
    main()
