#Ethernet configuration

The Raspberry Pi uses dhcpcd to configure its network interfaces, including assigning IP addresses using either DHCP or assigning a static IP address. The configuration is specified in the file /etc/dhcpcd.conf.

The GUI tool used by the Raspberry Pi desktop to allow the user to make changes to the network configuration is called lxplug-network and is based on dhcpcd-ui, which was developed by the same person who wrote dhcpcd.
