

#!/usr/bin/env python3

import time
import os
import logging
from logging.handlers import RotatingFileHandler  # Importing necessary modules

# This sets up defined logging format and levels
log_format = "%(asctime)s - %(levelname)s - %(message)s"  # Define logging format
logging.basicConfig(level=logging.DEBUG, format=log_format)  # Set up logging configuration

def ip_to_ping(t_ip):
    try:
        response = ping(t_ip, timeout=1)  # Ping the target IP with a timeout of 1 second
        return response is not None  # Return True if response is received, indicating host is up
    except PingError as e:
        logging.error(f"Ping error occurred: {e}")  # Log an error if ping operation fails
        return False  # Return False indicating failure

def log_event(status, t_ip, log_filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Get current timestamp
    log_entry = f"{timestamp} Network {'Active' if status else 'Inactive'} to {t_ip}"  # Format log entry
    
    # If log file size exceeds 20 bytes, rotate the logs
    if os.path.getsize(log_filename) > 20:
        rotate_logs(log_filename)  # Rotate logs if file size exceeds threshold
    
    with open(log_filename, 'a') as log_file:  # Open log file in append mode
        log_file.write(log_entry + '\n')  # Write log entry to the log file
    logging.info(log_entry)  # Log the event at INFO level

def rotate_logs(log_filename):
    backup_count = 5  # Define the number of backup logs to keep
    if os.path.exists(log_filename):  # Check if the log file exists
        for i in range(backup_count - 1, 0, -1):  # Iterate over the backup logs
            src = f"{log_filename}.{i}"  # Define source file name
            dest = f"{log_filename}.{i + 1}"  # Define destination file name
            if os.path.exists(src):  # Check if the source file exists
                os.rename(src, dest)  # Rename the source file to the destination file
        os.rename(log_filename, f"{log_filename}.1")  # Rename the log file to .1 (the first backup)

def main():
    logging.info("Welcome to the Uptime Sensor Tool. This script will evaluate if a host is up or down on the Local Area Network (LAN).")
    logging.info("The sensor tool will ping continuously, if you want to exit the tool please press ctrl + c.")
    
    t_ip = input("Please enter an IP address on the LAN: ")  # Prompt user to enter an IP address
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Get the path to the desktop
    log_filename = os.path.join(desktop_path, f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")  # Define log file name
    
    while True:  # Main loop for continuous pinging
        try:
            status = ip_to_ping(t_ip)  # Ping the target IP
            log_event(status, t_ip, log_filename)  # Log the event
            time.sleep(2)  # Wait for 2 seconds before the next iteration
        except KeyboardInterrupt:  # Handle keyboard interrupt
            logging.info("User interrupted the script. Exiting...")  # Log a message
            break  # Exit the loop

if __name__ == "__main__":
    main()  # Execute the main function if the script is run directly
