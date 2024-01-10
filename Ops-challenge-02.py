# Script Name:					Uptime Sensor Tool
# Author: 					    Juan Maldonado
# Date of latest revision:		1/9/2023
# Purpose:					    This script is an uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down.

# For time-related functions
import time  

# For working with date and time
# Documentation for this can be found in https://docs.python.org/3/library/datetime.html
from datetime import datetime  

# For working with the operating system (path, file operations)
import os  

# Third-party library for ICMP ping operations
# Documentation for this can be found on https://github.com/kyan001/ping3/blob/master/README.md
from ping3 import ping  

def ip_to_ping(target_ip):
    response = ping(target_ip, timeout=1)
    return response is not None

def log_event(status, target_ip):
     # This gets the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # This formats the log entry
    log_entry = f"{timestamp} Network {'Active' if status else 'Inactive'} to {target_ip}"

    # This creates a log file in the Documents folder with a timestamped name
    # The file name could be called for example: ping_log_20240110_153045.txt, the first set of numbers will be the date, the second will be military time (24h)
    # This will also append the log entry to the log file
    log_filename = os.path.join(os.path.expanduser("~"), "Documents", f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_filename, 'a') as log_file:
        log_file.write(log_entry + '\n')
    
    # Print the log entry
    print(log_entry)

def main():
    # Welcome message for user
    print("Welcome to the Uptime Sensor Tool. This script will evaluate if a host is up or down on the Local Area Network (LAN).")
    print("The sensor tool will ping continuously, if you want to exit the tool please press ctrl + c.")
    # This accepts user input for the target IP address
    target_ip = input("Please enter an IP address on the LAN: ")

    # This loops is used to ping the target every two seconds
    while True:
        # Ping the target and get the status
        status = ip_to_ping(target_ip)

        # Log the event with timestamp, target IP, and status
        log_event(status, target_ip)

        # This allows us to wait for two seconds before the next iteration
        time.sleep(2)

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
