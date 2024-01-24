from scapy.all import *
import random
from ipaddress import ip_network

def scan_port(ip, port):
    # Same as before

def scan_ports(ip, port_range):
    for port in range(port_range[0], port_range[1] + 1):
        scan_port(ip, port)

def icmp_ping_sweep(network_address):
    network = ip_network(network_address, strict=False)
    live_hosts = []

    for ip in network.hosts():
        response = sr1(IP(dst=str(ip))/ICMP(), timeout=1, verbose=0)
        if response is not None and response.haslayer(ICMP) and response.getlayer(ICMP).type == 0:
            print(f"Host {ip} is reachable.")
            live_hosts.append(ip)

    return live_hosts

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
