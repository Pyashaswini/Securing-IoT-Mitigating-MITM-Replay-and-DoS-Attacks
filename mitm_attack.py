from scapy.all import sniff, IP, TCP, Raw, get_if_list
import os

# Define the IP addresses of the client and server
client_ip = ''
server_ip = ''

# Directory to save captured files
output_dir = "captured_files"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def filter_data_packets(packet, seen_payloads):
    """Filter packets to capture only the unique payloads between client and server"""
    if packet.haslayer(TCP) and packet.haslayer(Raw) and \
       ((packet[IP].src == client_ip and packet[IP].dst == server_ip) ):

        payload = packet[Raw].load
        if payload not in seen_payloads:
            seen_payloads.add(payload)
            return True
    return False

def save_packets_to_file(packets, filename="captured_file_data.txt"):
    """Save the raw data packets to a file"""
    with open(filename, 'ab') as f:
        for packet in packets:
            if packet.haslayer(Raw):
                f.write(packet[Raw].load)  # Save raw payload

def capture_and_save():
    """Capture and save packets containing file data"""
    seen_payloads = set()
    print("Available network interfaces:", get_if_list())
    print("Capturing packets...")

    # Capture packets, filter the data, and save the payload to a file
    packets = sniff(filter="tcp", lfilter=lambda x: filter_data_packets(x, seen_payloads),
                    count=100, iface="eth0", timeout=30)  # Replace with the correct interface

    if not packets:
        print("No unique packets with data payload captured.")
        return

    # Save the captured packets' raw data to a file
    output_filename = os.path.join(output_dir, "captured_file_data.txt")
    save_packets_to_file(packets, output_filename)
    print(f"Captured packets saved to {output_filename}")

if __name__ == '__main__':
    capture_and_save()
