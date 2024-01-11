# If you are running this script on a Linux environment such as Ubuntu
# please uncomment the shebang line and the log_filename variable 
# #!/usr/bin/env python3

# Script Name:					   Uptime Sensor Tool part 2
# Author: 					       Juan Maldonado
# Date of latest revision:		   1/10/2023
# Purpose:					       This script is an uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down. And sends an email notification. 

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

# This is a module for sending emails
import smtplib

# this allows the creation of email content
from email.mime.text import MIMEText

# This is the email configuration
# This is a burner email that will recive the notification 
recipient_email = 'johncruzzz1996@gmail.com'

# This checks if ip can be pinged 
def ip_to_ping(target_ip):
    response = ping(target_ip, timeout=1)
    return response is not None

# This logs an event to a txt file
def log_event(target_ip, target_hostname, timestamp, status):
    # This formats the log entry
    log_entry = f"{timestamp} - Host {target_ip} ({target_hostname} is { 'up' if status else 'down'})"

    # This creates a log file in the Documents folder with a timestamped name
    # The file name could be called for example: ping_log_20240110_153045.txt, the first set of numbers will be the date, the second will be military time (24h)

    # For Linux environment uncomment the log_filename variable below (line 38) and comment the log_filename variable (line 39) 
    # log_filename = os.path.join(os.path.expanduser("~"), f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    log_filename = os.path.join(os.path.expanduser("~"), "Documents", "event_log.txt")
    with open(log_filename, 'a') as log_file:
        log_file.write(log_entry + '\n')
    
    # Print the log entry
    print(log_entry)

# This sends email notification using a localhost SMTP server
def send_email(subject, body):

    msg = MIMEText(body)
    msg[ 'Subject' ] = subject
    msg[ 'From' ] = 'sender@example.com'
    msg[ 'To' ] = recipient_email

    with smtplib.SMTP('localhost') as server:
        server.sendmail('sender@example.com', [recipient_email], msg.as_string())


def main():
    # Welcome message for user
    print("Welcome to the Uptime Sensor Tool. This script will evaluate if a host is up or down on the Local Area Network (LAN).")
    print("The sensor tool will ping continuously, if you want to exit the tool please press ctrl + c.")
    
    # This accepts user input for the target IP address
    target_ip = input("Please enter an IP address of a host on the LAN: ")
    target_hostname = input("Please enter the hostname associated with the IP address you entered:  ")
   
    # This loops is used to ping the target every two seconds
    while True:
        status = ip_to_ping(target_ip)

        if hasattr(main, "previous_status") and main.previous_status != status:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_event(target_ip, target_hostname, timestamp, status)

            subject = f"Host Status Changed: {target_ip} ({target_hostname})"
            body = f"Host status changed at {timestamp}\n\nPrevious Status: {'Up' if main.previous_status else 'Down'}\nCurrent Status: {'Up' if status else 'Down'}"
            send_email(subject, body)
        
        main.previous_status = status
        time.sleep(2)

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
