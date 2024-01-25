# If you are running on bash, uncomment the next line
# #!/bin/bash

# Script Name:					Ops-401d12.py
# Author: 					    Juan Maldonado
# Date of latest revision:		1/24/2024
# Purpose:					    This script is a network security tool pings an IP address determined by the user.
#                       If the host exists, scan its ports and determine if any are open.


# Before running this code on VScode please do the following:
# on the command terminal, run the command pip install scapy
# If using a linux os, run the command sudo apt-get update & sudo apt-get install python3-scapy

# Documentation for scapy use is found on this website: https://scapy.readthedocs.io/en/latest/usage.html#sending-packets
from scapy.all import *
import random
# Documentation for ipaddress use is found on this website: https://docs.python.org/3/library/ipaddress.html
from ipaddress import ip_network

# This scans a specific TCP port
def scan_port(ip, port):
    # Same as before

# This scans a range of TCP ports
def scan_ports(ip, port_range):
    for port in range(port_range[0], port_range[1] + 1):
        scan_port(ip, port)

# This perfroms ICMP Ping Sweep
def icmp_ping_sweep(network_address):
    network = ip_network(network_address, strict=False)
    live_hosts = []

    for ip in network.hosts():
        # This sends an ICMP echo requests and waits for a respinse (will wait one sec)
        response = sr1(IP(dst=str(ip))/ICMP(), timeout=1, verbose=0)
        if response is not None and response.haslayer(ICMP) and response.getlayer(ICMP).type == 0:
            print(f"Host {ip} is reachable.")
            live_hosts.append(ip)

    return live_hosts

# This scans and pings the ip
def ping_and_scan_ports(target_ip):
    # This sends an ICMP Ping to the target IP
    response = sr1(IP(dst=target_ip)/ICMP(), timeout=1, verbose=0)
    
    # This checks if a response is received and it's an ICMP Echo Reply (type 0)
    if response is not None and response.haslayer(ICMP) and response.getlayer(ICMP).type == 0:
        print(f"Host {target_ip} is reachable. Scanning ports...")
        
        
        default_port_range = (1, 1024)
        
        # This scans the ports within the specified range
        scan_ports(target_ip, default_port_range)
    else:
        print(f"Host {target_ip} is unreachable.")
def main():
    print("Select mode:")
    print("1. TCP Port Range Scanner mode")
    print("2. ICMP Ping Sweep mode")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        host_ip = input("Enter the target IP address: ")
        port_range = tuple(map(int, input("Enter the port range (start end): ").split()))
        scan_ports(host_ip, port_range)
    elif choice == "2":
        network_address = input("Enter the network address with CIDR block (e.g., 10.10.0.0/24): ")
        live_hosts = icmp_ping_sweep(network_address)
        print("List of live hosts:")
        for host in live_hosts:
            print(host)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
