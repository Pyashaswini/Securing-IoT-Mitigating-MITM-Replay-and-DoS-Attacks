System Setup
Devices:

Two Raspberry Pi devices:
One acts as the server, hosting data and handling client requests.
The other acts as the client, sending legitimate requests to the server.
A third system (Kali Linux VM) simulates the attacker in all scenarios.
Attack Mechanisms:

DoS: A Python script floods the server with requests.
MITM: ARP spoofing redirects client-server communication through the attacker.
Replay: The attacker captures and replays previously sent packets using packet-capturing tools like Scapy.
Network:

Devices communicate over a shared wireless network.
IP addresses and MAC addresses are manipulated during attacks to simulate vulnerabilities.

Communication Flow
Raspberry Pi 1 (Server) is configured to receive client requests, and after authentication, it serves the requested files or data.
Raspberry Pi 2 (Client) initiates requests (e.g., login credentials or file access) to the server.
Laptop 1 (Kali Linux VM) performs ARP spoofing to intercept communication between the server and client. Additionally, it executes DoS and MITM attacks.
Laptop 2 is used to monitor the server-client communication through VNC or other tools (such as Wireshark) to inspect traffic and analyze attacks.

Attack Setup and Goals
In this project, we set up a network scenario where a client and a server communicate over a local network. The goal was to demonstrate and analyze three types of attacks: Denial-of-Service (DoS), Man-in-the-Middle (MITM), and Replay. The attacker in this scenario used ARP spoofing to intercept and manipulate communication between the client and server.
1. Denial-of-Service (DoS) Attack
What We Aimed to Do:
The goal of the DoS attack was to overwhelm the server by flooding it with excessive requests, causing it to become unresponsive to legitimate traffic.
What We Achieved:
Using a script that initiates multiple connections from a single IP, we were able to send an overwhelming number of requests to the server in a short period.
The server could not differentiate between legitimate and malicious requests, and as a result, it was temporarily overwhelmed and unresponsive to normal traffic.
Detection and Prevention:
Detection: By tracking the number of connections from each IP address over a 10-second window, we successfully flagged suspicious activity when an IP address exceeded the connection threshold.
Prevention: We implemented rate limiting to block or limit connections from IPs exceeding the threshold, which reduced server strain and protected against potential DoS attacks.


2. Man-in-the-Middle (MITM) Attack
What We Aimed to Do:
The objective of the MITM attack was to intercept and capture sensitive information, such as usernames, passwords, and files, being exchanged between the client and server.
What We Achieved:
By using ARP spoofing, the attacker successfully intercepted communication between the client and server, including login credentials.
Login Credentials: We captured the username and password transmitted from the client to the server.
Files: We intercepted and examined files being transferred between the client and server, and these files were readable during the attack.
Outcome and Real-World Implication:
While we could read the captured files, in a real-world scenario, communication would typically be protected with encryption methods like SSH or TLS.
Secure transmission methods (e.g., SSH) would render the intercepted data unreadable without proper decryption keys, which would protect sensitive information such as usernames, passwords, and files.
This highlights the importance of implementing proper encryption and secure communication channels in protecting against MITM attacks.


3. Replay Attack
What We Aimed to Do:
The objective of the replay attack was to capture a legitimate message (such as a login or file transfer request) and resend it to the server to simulate a legitimate action, potentially allowing unauthorized access or repeated actions.
What We Achieved:
We successfully captured network packets from the client-server communication and attempted to replay the captured packets to the server.
However, while we could observe the data, replaying the captured messages was unsuccessful in this case, as the server effectively handled the repeated messages.
Likely reasons for failure include:
Session-specific identifiers: The server expected unique session tokens or other context-sensitive data.
Sequence number mismatch: The replayed packets didn't match the current TCP session state.
Timing issues: The server rejected outdated packets.
Detection and Prevention:
Detection: We could have implemented a detection mechanism by using timestamps to track the freshness of incoming messages.
Prevention: To prevent replay attacks, timestamps could be included in each message to ensure that any replayed message, if received after a certain time threshold, would be flagged and rejected.


Summary
DoS Attack: We were able to overwhelm the server with excessive requests, and the rate-limiting mechanism effectively mitigated the attack by blocking malicious connections.
MITM Attack: The attacker successfully intercepted and read sensitive information like usernames, passwords, and files. However, in a secure environment, encryption would protect the data, preventing unauthorized access to captured information.
Replay Attack: While we captured valid communication, we were unable to replay the messages successfully due to network issues and lack of timestamp validation. In a real-world system, adding timestamp checks would prevent replay attacks.
