# Script Name:					Event Logging Tool
# Author: 					    Juan Maldonado
# Date of latest revision:		2/12/2024
# Purpose:					    This script is incorporating logging capabilities into one of my existing Python tools (an uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down).

#!/usr/bin/env python3
# These are all necessary modules
import time  # This is for time-related functions
from datetime import datetime  # This is for working with date and time
import os  # This is for working with the operating system (path, file operations), I used it on a windows 10 pro

# resource: https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
import logging  # This is for logging capabilities
from ping3 import ping, PingError  # This is a third-party library for ICMP ping operations

# This sets up defined logging format and levels
# resource: https://docs.python.org/3/howto/logging.html#formatters
log_format = "%(asctime)s - %(levelname)s - %(message)s"  # This defines logging format
logging.basicConfig(level=logging.DEBUG, format=log_format)  # This sets the logging configuration

# This defines the function to ping a target IP address
def ip_to_ping(t_ip):
    try:
        response = ping(t_ip, timeout=1)  # This pings a target IP with a timeout of 1 second
        return response is not None  # This returns True if response is received, False otherwise
    except PingError as e:
        logging.error(f"Ping error occurred: {e}")  # This records a Log error if ping operation fails
        return False  # This returns a False indicating failure

# This defines a function that logs events
def log_event(status, t_ip):
    # This gets the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    # This formats a log entry
    log_entry = f"{timestamp} Network {'Active' if status else 'Inactive'} to {t_ip}"

    # This defines a log file path on desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    log_filename = os.path.join(desktop_path, f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    # This writes a log entry to the newly created log file
    with open(log_filename, 'a') as log_file:
        log_file.write(log_entry + '\n')
    
    # This logs an event at INFO level
    logging.info(log_entry)

# This defines the main function
def main():
    # This is a welcome message
    logging.info("Welcome to the Uptime Sensor Tool. This script will evaluate if a host is up or down on the Local Area Network (LAN).")
    logging.info("The sensor tool will ping continuously, if you want to exit the tool please press ctrl + c.")
    
    # This gets a target IP address from user via input
    t_ip = input("Please enter an IP address on the LAN: ")

    # This loops for pinging the target IP
    while True:
        try:
            # This pings the target IP and get status
            status = ip_to_ping(t_ip)
            # This logs the event as it happens
            log_event(status, t_ip)
            # Wait for 2 seconds before the next iteration
            time.sleep(2)
        except KeyboardInterrupt:
            # This logs a message if user interrupts the script
            logging.info("User interrupted the script. Exiting...")
            break  # Exit the loop

# This executes the main function if the script is run directly
if __name__ == "__main__":
    main()
