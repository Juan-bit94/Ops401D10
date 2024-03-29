# Script Name:					Event Logging Tool & log rotation and email
# Author: 					    Juan Maldonado
# Date of latest revision:		2/14/2024
# Purpose:					    This script has incorporating logging capabilities into one of my existing Python tools (an uptime sensor tool that uses ICMP packets to evaluate if hosts on the LAN are up or down).
#                               Now it has a new log rotation feature based on size and will email user notifications of an error issue. 

#!/usr/bin/env python3

import time  # This imports the time module for timing operations
import os  # This imports the os module for interacting with the operating system
import logging  # This imports the logging module for logging events
from logging.handlers import RotatingFileHandler, SMTPHandler  # This imports necessary handlers for logging
from datetime import datetime  # This imports the datetime module for timestamp

log_format = "%(asctime)s - %(levelname)s - %(message)s"  # This defines the log format
logging.basicConfig(level=logging.DEBUG, format=log_format)  # This sets up a basic logging configuration

def ip_to_ping(t_ip):
    try:
        # This is a placeholder for ping function
        return True  # This assumes a ping is successful 
    except Exception as e:
        logging.error(f"Ping error occurred: {e}")  # This logs a ping error
        return False

def setup_logging(log_filename, email):
    rotating_handler = RotatingFileHandler(log_filename, maxBytes=20000, backupCount=5)  # This creates a rotating file handler
    rotating_handler.setFormatter(logging.Formatter(log_format))  # This sets a log format for rotating handler
    rotating_handler.setLevel(logging.INFO)  # This sets a logging level for rotating handler
    
    stream_handler = logging.StreamHandler()  # This creates the stream handler for logging to console
    stream_handler.setFormatter(logging.Formatter(log_format))  # This sets a log format for stream handler
    stream_handler.setLevel(logging.INFO)  # This sets a logging level for the stream handler

    # This is for email configurations. Please add your email if you use gmail. 
    email_handler = SMTPHandler(  # This creates a SMTP handler for sending emails
        mailhost=("smtp.gmail.com", 587),  # Change to your SMTP server details
        fromaddr="johncruzzz1996@gmail.com",  # Change to your email address
        toaddrs=email,  # Set recipient's email address
        subject="Uptime Sensor Alert",  # Email subject
        credentials=("johncruzzz1996@gmail.com", "password")  # Change to your SMTP credentials
    )
    email_handler.setLevel(logging.ERROR)  # This sets the logging level for email handler

    logger = logging.getLogger()  # This gets the root logger instance
    logger.addHandler(rotating_handler)  # This adds rotating file handler to logger
    logger.addHandler(stream_handler)  # This adds stream handler to logger
    logger.addHandler(email_handler)  # This adds an email handler to logger

def log_event(status, t_ip, log_filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # This gets the current timestamp
    log_entry = f"{timestamp} Network {'Active' if status else 'Inactive'} to {t_ip}"  # This formats a log entry
    
    if os.path.getsize(log_filename) > 20:  # This checks a log file size
        rotate_logs(log_filename)  # This rotates the logs if size exceeds threshold
    
    with open(log_filename, 'a') as log_file:  # This opens the log file in append mode
        log_file.write(log_entry + '\n')  # This writes a log entry to log file
    logging.info(log_entry)  # This logs an event at INFO level

def rotate_logs(log_filename):
    backup_count = 5  # This defines a number of backup logs to keep
    if os.path.exists(log_filename):  # This checks if a log file exists
        for i in range(backup_count - 1, 0, -1):  # This iterates over the backup logs
            src = f"{log_filename}.{i}"  # This defines a source file name
            dest = f"{log_filename}.{i + 1}"  # This defines a destination file name
            if os.path.exists(src):  # This checks if a source file exists
                os.rename(src, dest)  # This renames source file to destination file
        os.rename(log_filename, f"{log_filename}.1")  # This renames a log file to .1 (the first backup)

def main():
    logging.info("Welcome to the Uptime Sensor Tool. This script will evaluate if a host is up or down on the Local Area Network (LAN).")
    logging.info("The sensor tool will ping continuously, if you want to exit the tool please press ctrl + c.")
    
    t_ip = input("Please enter an IP address on the LAN: ")  # This prompts a user to enter IP address
    email = input("Please enter your email address to receive alerts: ")  # This prompts a user to enter email address
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # This gets a path to desktop
    log_filename = os.path.join(desktop_path, f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")  # This defines a log file name
    
    setup_logging(log_filename, email)  # This sets up a logging with handlers
    
    while True:  # This is the main loop for continuous pinging
        try:
            status = ip_to_ping(t_ip)  # This pings the target IP
            log_event(status, t_ip, log_filename)  # This logs the event
            time.sleep(2)  # This waits for 2 seconds before next iteration
        except KeyboardInterrupt:  # This handles any keyboard interrupt
            logging.info("User interrupted the script. Exiting...")  # This is the log message
            break  # Exit the loop

if __name__ == "__main__":
    main()  # This executes the main function if script is run directly
