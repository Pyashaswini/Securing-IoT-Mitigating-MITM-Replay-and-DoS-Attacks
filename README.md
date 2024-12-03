# System Setup and Attack Analysis

## Overview

This project demonstrates the setup and analysis of three types of attacks: 
1. **Denial-of-Service (DoS)**  
2. **Man-in-the-Middle (MITM)**  
3. **Replay**  

The setup consists of two Raspberry Pi devices acting as the client and server, while a third system (Kali Linux VM) simulates the attacker. The goal is to explore the mechanics of these attacks, their potential impact, and the methods to detect and prevent them in real-world scenarios.

---

## Devices

- **Raspberry Pi 1 (Server)**  
  - **Role**: Hosts data and handles client requests (e.g., authentication, file serving).

- **Raspberry Pi 2 (Client)**  
  - **Role**: Sends legitimate requests to the server (e.g., login credentials, file access).

- **Laptop 1 (Kali Linux VM - Attacker)**  
  - **Role**: Simulates the attacker and executes DoS, MITM, and Replay attacks.

- **Laptop 2 (Monitoring)**  
  - **Role**: Monitors server-client communication and analyzes attacks using tools like VNC and Wireshark.

---

## Attack Mechanisms

1. **Denial-of-Service (DoS)**  
   A Python script floods the server with excessive requests, making it unresponsive to legitimate traffic.

2. **Man-in-the-Middle (MITM)**  
   ARP spoofing redirects communication between the client and server through the attacker, enabling interception of data.

3. **Replay**  
   The attacker captures and replays previously sent packets to simulate legitimate requests, potentially gaining unauthorized access.

---

## Network Setup

The devices communicate over a shared wireless network. During attacks, IP and MAC addresses are manipulated to simulate vulnerabilities exploited by attackers.

---

## Communication Flow

- **Raspberry Pi 1 (Server)**: Receives client requests and provides requested data upon successful authentication.  
- **Raspberry Pi 2 (Client)**: Initiates requests to the server (e.g., login credentials, file access).  
- **Laptop 1 (Kali Linux VM - Attacker)**: Executes ARP spoofing, DoS, and MITM attacks.  
- **Laptop 2 (Monitoring)**: Observes and analyzes communication using tools like VNC and Wireshark.  

---

## Attack Setup and Goals

### 1. Denial-of-Service (DoS) Attack

- **Objective**: Overwhelm the server with excessive requests to render it unresponsive to legitimate traffic.  
- **What Was Achieved**:  
  - Flooded the server with requests using a Python script.  
  - Server became temporarily unresponsive.  
- **Detection and Prevention**:  
  - **Detection**: Tracked excessive connections from individual IP addresses.  
  - **Prevention**: Implemented rate limiting to block IPs exceeding a set threshold.

---

### 2. Man-in-the-Middle (MITM) Attack

- **Objective**: Intercept sensitive information (e.g., usernames, passwords, and files) exchanged between the client and server.  
- **What Was Achieved**:  
  - ARP spoofing allowed interception of communication, capturing login credentials and files.  
- **Detection and Prevention**:  
  - **Detection**: Monitored suspicious traffic patterns and verified data integrity.  
  - **Prevention**: Implemented AES encryption and server-side authentication to ensure intercepted data was unreadable.  

---

### 3. Replay Attack

- **Objective**: Capture legitimate communication (e.g., login requests or file access) and replay it to simulate valid actions.  
- **What Was Achieved**:  
  - Captured packets during communication.  
  - Replaying packets failed due to session-specific identifiers and timing mismatches.  
- **Detection and Prevention**:  
  - **Detection**: Used timestamps and session tokens to ensure message freshness.  
  - **Prevention**: Rejected outdated or repeated messages via timestamp and session validation.  

---

## Conclusion

- **DoS Attack**: Successfully overwhelmed the server but mitigated using rate limiting to block excessive connections.  
- **MITM Attack**: Intercepted sensitive information; encryption and secure protocols (e.g., SSH) can protect against such attacks in real-world scenarios.  
- **Replay Attack**: While communication was captured, replay attempts failed due to session-specific validation.  

---

## Requirements

- Raspberry Pi devices (or equivalent devices capable of running Python)  
- Kali Linux VM for attack simulations  
- Python (for attack scripts)  
- Wireshark or similar tools for packet analysis  
- VNC or other remote desktop tools for monitoring communication  
