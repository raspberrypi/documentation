# TCP/IP networking

The Raspberry Pi uses dhcpcd to configure TCP/IP across all of its network interfaces. The dhcpcd daemon was written by Roy Marples and is intended to be an all-in-one ZeroConf client for UNIX-like systems. This includes assigning each interface an IP address, setting netmasks and configuring DNS resolution via the Name Service Switch (NSS) facility. The configuration of the dhcpcd daemon is specified in the file `/etc/dhcpcd.conf`. To configure the dhcpcd daemon, refer to [ArchWiki's dhcpcd page](https://wiki.archlinux.org/index.php/Dhcpcd).

On Raspberry Pi systems where the graphical desktop is installed, a GUI tool called lxplug-network is used to allow the user to make changes to the configuration of dhcpcd. The lxplug-network tool is based on dhcpcd-ui, which was also developed by Roy Marples.
