# TCP/IP networking

The Raspberry Pi uses `dhcpcd` to configure TCP/IP across all of its network interfaces. The dhcpcd daemon was written by Roy Marples and is intended to be an all-in-one ZeroConf client for UNIX-like systems. This includes assigning each interface an IP address, setting netmasks, and configuring DNS resolution via the Name Service Switch (NSS) facility. 

By default, Raspberry Pi OS attempts to automatically configure all network interfaces by DHCP, falling back to automatic private addresses in the range 169.254.0.0/16 if DHCP fails. This is consistent with the behaviour of other Linux variants and of Microsoft Windows.

## Static IP address

If you wish to disable automatic configuration for an interface and instead configure it statically, add the details to `/etc/dhcpcd.conf`. For example:

```
interface eth0
static ip_address=192.168.0.4/24	
static routers=192.168.0.254
static domain_name_servers=192.168.0.254 8.8.8.8
```

You can find the names of the interfaces present on your system using the `ip link` command.

Note that if you have several Raspberry Pis connected to the same network, you may find it easier instead to set address reservations on your DHCP server. In this way, each Pi will keep the same IP address, but they will all be managed in one place, making reconfiguring your network in the future more straightforward.

On Raspberry Pi systems where the graphical desktop is installed, a GUI tool called `lxplug-network` is used to allow the user to make changes to the configuration of `dhcpcd`, including setting static IP addresses. The `lxplug-network` tool is based on `dhcpcd-ui`, which was also developed by Roy Marples.
