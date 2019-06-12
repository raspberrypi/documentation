#Ethernet configuration

The Raspberry Pi uses dhcpcd to configure its network interfaces. The dhcpcd daemon was written by Roy Marples and is intended to be an all-in-one ZeroConf client for UNIX-like systems. On the Raspberry Pi it is used to configure the TCP/IP suite of network protocols across all interfaces by default. This includes assigning each interface an IP address, setting netmasks and configuring DNS resolution via the Name Service Switch (NSS) facility. The configuration of the dhcpcd daemon is specified in the file `/etc/dhcpcd.conf`.

On Raspberry Pi systems where the graphical desktop is installed, a GUI tool called lxplug-network is used to allow the user to make changes to the configuration of dhcpcd. The lxplug-network tool is based on dhcpcd-ui, which was also developed by Roy Marples.
