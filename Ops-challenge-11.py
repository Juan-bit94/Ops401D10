from scapy.all import *
import random

def scan_port(ip, port):
    src_port = random.randint(1025, 65535)  # Randomize source port
    response = sr1(IP(dst=ip)/TCP(sport=src_port, dport=port, flags="S"), timeout=1, verbose=0)

    if response is None:
        print(f"Port {port} is filtered (silently dropped).")
    elif response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:
            send(IP(dst=ip)/TCP(sport=src_port, dport=port, flags="R"), verbose=0)
            print(f"Port {port} is open.")
        elif response.getlayer(TCP).flags == 0x14:
            print(f"Port {port} is closed.")
    else:
        print(f"Unable to determine the status of port {port}.")

def scan_ports(ip, port_range):
    for port in range(port_range[0], port_range[1] + 1):
        scan_port(ip, port)

# Example usage
host_ip = "127.0.0.1"
ports_to_scan = (80, 100)  # Specify the port range

scan_ports(host_ip, ports_to_scan)
