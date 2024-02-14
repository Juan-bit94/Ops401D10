# Script Name:					Event Logging Tool & log rotation
# Author: 					    Juan Maldonado
# Date of latest revision:		2/13/2024
# Purpose:					    This script has incorporating logging capabilities into one of my existing Python tools (an uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down).
#                               Now it has a new log rotation feature based on size
#!/usr/bin/env python3

import time
import os
import logging
from logging.handlers import RotatingFileHandler  # This imports necessary modules

# This sets up defined logging format and levels
log_format = "%(asctime)s - %(levelname)s - %(message)s"  # This defines a logging format
logging.basicConfig(level=logging.DEBUG, format=log_format)  # This sets up a logging configuration

def ip_to_ping(t_ip):
    try:
        response = ping(t_ip, timeout=1)  # This pings the target IP with a timeout of 1 second
        return response is not None  # This returns a True if response is received, indicating host is up
    except PingError as e:
        logging.error(f"Ping error occurred: {e}")  # This logs an error if ping operation fails
        return False  # This returns a False indicating failure

def log_event(status, t_ip, log_filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # This gets a current timestamp
    log_entry = f"{timestamp} Network {'Active' if status else 'Inactive'} to {t_ip}"  # This formats a log entry
    
    # So if a log file size exceeds 20 bytes, it rotates the logs
    if os.path.getsize(log_filename) > 20:
        rotate_logs(log_filename)  # This rotates the logs if file size exceeds threshold
    
    with open(log_filename, 'a') as log_file:  # Open log file in append mode
        log_file.write(log_entry + '\n')  # This writes a log entry to the log file
    logging.info(log_entry)  # This logs the event at INFO level

def rotate_logs(log_filename):
    backup_count = 5  # This defines the number of backup logs to keep
    if os.path.exists(log_filename):  # This checks if the log file exists
        for i in range(backup_count - 1, 0, -1):  # This just iterates over the backup logs
            src = f"{log_filename}.{i}"  # This defines a source file name
            dest = f"{log_filename}.{i + 1}"  # This defines a destination file name
            if os.path.exists(src):  # This checks if the source file exists
                os.rename(src, dest)  # This renames the source file to the destination file
        os.rename(log_filename, f"{log_filename}.1")  # This renames the log file to .1 (the first backup)

def main():
    logging.info("Welcome to the Uptime Sensor Tool. This script will evaluate if a host is up or down on the Local Area Network (LAN).")
    logging.info("The sensor tool will ping continuously, if you want to exit the tool please press ctrl + c.")
    
    t_ip = input("Please enter an IP address on the LAN: ")  # This prompts a user to enter an IP address
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # This gets the path to the desktop
    log_filename = os.path.join(desktop_path, f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")  # This defines a log file name
    
    while True:  # This is a main loop for continuous pinging
        try:
            status = ip_to_ping(t_ip)  # This pings the target IP
            log_event(status, t_ip, log_filename)  # This logs an event
            time.sleep(2)  # This waits for 2 seconds before the next iteration
        except KeyboardInterrupt:  # This handles any keyboard interrupts
            logging.info("User interrupted the script. Exiting...")  # This logs a message
            break  # This exits the loop

if __name__ == "__main__":
    main()  # This executes the main function if the script is run directly
