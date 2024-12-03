System Setup and Attack Analysis
Overview
This project demonstrates the setup and analysis of three types of attacks: Denial-of-Service (DoS), Man-in-the-Middle (MITM), and Replay. The setup consists of two Raspberry Pi devices acting as the client and server, while a third system (Kali Linux VM) simulates the attacker. The goal is to explore how these attacks work, what they can achieve, and how to detect and prevent them in a real-world scenario.

System Setup
Devices
Raspberry Pi 1 (Server):

Role: Hosts data and handles client requests, such as authentication and file serving.
Raspberry Pi 2 (Client):

Role: Sends legitimate requests to the server (e.g., login credentials, file access).
Laptop 1 (Kali Linux VM - Attacker):

Role: Simulates the attacker and executes DoS, MITM, and Replay attacks.
Laptop 2 (Monitoring):

Role: Monitors the server-client communication and analyzes attacks using VNC, Wireshark, or other monitoring tools.
Attack Mechanisms
Denial-of-Service (DoS): A Python script floods the server with excessive requests, causing it to become unresponsive.
Man-in-the-Middle (MITM): ARP spoofing redirects communication between the client and server through the attacker, enabling them to intercept data.
Replay: The attacker captures and replays previously sent packets to simulate legitimate requests, potentially gaining unauthorized access.
Network Setup
The devices communicate over a shared wireless network. During the attacks, IP addresses and MAC addresses are manipulated to simulate vulnerabilities that attackers could exploit.

Communication Flow
Raspberry Pi 1 (Server): Configured to receive client requests and provide requested data after successful authentication.
Raspberry Pi 2 (Client): Initiates requests to the server (such as login credentials or file access).
Laptop 1 (Kali Linux VM - Attacker): Performs ARP spoofing to intercept communication between the client and server. It also executes DoS and MITM attacks.
Laptop 2: Used for monitoring communication between the server and client through tools like VNC and Wireshark.
Attack Setup and Goals
1. Denial-of-Service (DoS) Attack
Objective: The goal of the DoS attack was to overwhelm the server by flooding it with excessive requests, causing it to become unresponsive to legitimate traffic.

What Was Achieved:

A Python script was used to send an overwhelming number of requests to the server.
The server was unable to differentiate between legitimate and malicious requests, resulting in temporary unresponsiveness.
Detection and Prevention:

Detection: Suspicious activity was flagged by tracking the number of connections from each IP address.
Prevention: Rate limiting was implemented to block IPs exceeding a threshold of connections, reducing server strain and mitigating the attack.
2. Man-in-the-Middle (MITM) Attack
Objective: The aim was to intercept sensitive information, such as usernames, passwords, and files, being exchanged between the client and server.

What Was Achieved:

ARP spoofing allowed the attacker to intercept client-server communication, including login credentials and file transfers.
The captured files were readable, and login credentials were successfully intercepted.
Outcome and Real-World Implication:

In a real-world environment, secure transmission (e.g., SSH or TLS encryption) would protect the data, making intercepted information unreadable without the proper decryption keys.
The project highlights the importance of implementing encryption to safeguard sensitive information against MITM attacks.
3. Replay Attack
Objective: The goal was to capture legitimate messages (e.g., login requests or file access) and replay them to the server, simulating a legitimate action to gain unauthorized access or repeat actions.

What Was Achieved:

The attacker successfully captured network packets during the client-server communication.
However, replaying the captured packets was unsuccessful due to session-specific identifiers, sequence number mismatches, or timing issues, preventing the server from accepting the replayed requests.
Detection and Prevention:

Detection: Detecting replay attacks could be done by tracking timestamps or session tokens to ensure that incoming messages are fresh.
Prevention: Implementing timestamp checks or session-based validation would prevent replay attacks by rejecting outdated or repeated messages.
Conclusion
DoS Attack: We successfully overwhelmed the server by flooding it with requests. The attack was mitigated by implementing rate limiting, which blocked excessive connections.
MITM Attack: Sensitive information such as usernames, passwords, and files were intercepted, but in a real-world scenario, secure transmission methods (e.g., SSH) would protect the data from unauthorized access.
Replay Attack: While we captured legitimate communication, the attack failed due to session handling and timing issues. In a real-world scenario, using timestamps or session identifiers would help detect and prevent replay attacks.
Requirements
Raspberry Pi devices (or any device capable of running Python)
Kali Linux VM for performing attacks
Python (for attack scripts)
Wireshark or similar tools for packet analysis
VNC or other remote desktop tools for monitoring communication
