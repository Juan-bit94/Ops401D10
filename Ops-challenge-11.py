# If you are running on bash, uncomment the next line
# #!/bin/bash

# Script Name:					Ops-challenge-11.py
# Author: 					    Juan Maldonado
# Date of latest revision:		1/22/2024
# Purpose:					    This script is a network security tool. It scans the network. 


from scapy.all import *
import random

# This function scans a specific port
def scan_port(ip, port):
    # This produces a randomized source port
    src_port = random.randint(1025, 65535)  # Randomize source port
    # This sends a SYN packet and waits for a response
    response = sr1(IP(dst=ip)/TCP(sport=src_port, dport=port, flags="S"), timeout=1, verbose=0)

    # This portion of the code is used to analyze the response 
    if response is None:
        print(f"Port {port} is filtered (silently dropped).")
    elif response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:
            # this sends a RST to close the connection if the SYN-ACK is recived
            send(IP(dst=ip)/TCP(sport=src_port, dport=port, flags="R"), verbose=0)
            print(f"Port {port} is open.")
        elif response.getlayer(TCP).flags == 0x14:
            print(f"Port {port} is closed.")
    else:
        print(f"Unable to determine the status of port {port}.")

# This scans a range of ports
def scan_ports(ip, port_range):
    for port in range(port_range[0], port_range[1] + 1):
        scan_port(ip, port)

# Main method
def main():
    host_ip = "127.0.0.1"
    # This specifices the port range
    ports_to_scan = (80, 100) 
    # This performs the port scan
    scan_ports(host_ip, ports_to_scan)

# This runs the main method
if __name == "__main__":
    main()
