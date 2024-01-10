import time  # For time-related functions
from datetime import datetime  # For working with date and time
import os  # For working with the operating system (path, file operations)
from ping3 import ping  # Third-party library for ICMP ping operations

def ping_target(target_ip):
    response = ping(target_ip, timeout=1)
    return response is not None

def log_event(status, target_ip):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the log entry
    log_entry = f"{timestamp} - Target: {target_ip} - Status: {'Success' if status else 'Failure'}"

    # Create a log file in the Documents folder with a timestamped name
    log_filename = os.path.join(os.path.expanduser("~"), "Documents", f"ping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    # Append the log entry to the log file
    with open(log_filename, 'a') as log_file:
        log_file.write(log_entry + '\n')

    # Print the log entry
    print(log_entry)

def main():
    # Accept user input for the target IP address
    target_ip = input("Enter the target IP address: ")

    # Main loop to ping the target every two seconds
    while True:
        # Ping the target and get the status
        status = ping_target(target_ip)

        # Log the event with timestamp, target IP, and status
        log_event(status, target_ip)

        # Wait for two seconds before the next iteration
        time.sleep(2)

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()
