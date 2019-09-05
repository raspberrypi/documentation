
# Setting up a Raspberry Pi as a Bridged Wireless Access Point

The Raspberry Pi can be used as a bridged wireless access point within an existing ethernet network. This will extend the network to wireless computers and devices.

```
                                         +- RPi -------+
                                     +---+ Bridge      |
                                     |   | WiFi AP     +-)))
                                     |   | 192.168.1.2 |         +- Laptop ----+
                                     |   +-------------+     (((-+ WiFi STA    |
                 +- Router ----+     |                           | 192.168.1.5 |
                 | Firewall    |     |   +- PC#2 ------+         +-------------+
(Internet)---WAN-+ DHCP server +-LAN-+---+ 192.168.1.3 |
                 | 192.168.1.1 |     |   +-------------+
                 +-------------+     |
                                     |   +- PC#1 ------+
                                     +---+ 192.168.1.4 |
                                         +-------------+

```

This can be done using the inbuilt wireless features of the Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access point mode.

Note that this documentation was tested on a Raspberry Pi 3, and it is possible that some USB dongles may need slight changes to their settings. If you are having trouble with a USB wireless dongle, please check the forums.

## Before you start

 * Ensure you have administrative access to your Raspberry Pi. The network setup will be entirely reset as part of the installation, so local access, with screen and keyboard connected to your Raspberry Pi is recommended. If installing remotely trhough SSH, be ready to add screen and keyboard in case you lose contact with your Raspberry Pi after the installation. 
 * Connect your Raspberry Pi to the ethernet network and boot the Raspbian OS. Ensure the Raspberry Pi has received its network configuration from a DHCP server on the network and so has Internet access.
 * Ensure the Raspbian OS on your Raspberry Pi is [up to date](../../raspbian/updating.md) and reboot if packages were installed in the process.
 * Have a wireless client ready to test your new access point.

## Install the access point software (hostapd)

In order to work as a bridged access point, the Raspberry Pi needs to have the `hostapd` access point software package installed:

```
sudo apt install hostapd
```
Enable the wireless access point service to start when your Raspberry Pi boots:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

This completes software installation. We will configure the access point software later on.

## Configure bridge networking

### Create a bridge device and populate the bridge (systemd-networkd)

Add a bridge network device called br0 in the system by creating the following file:

```
sudo nano /etc/systemd/network/bridge-br0.netdev

[NetDev]
Name=br0
Kind=bridge
```

In order to bridge the ethernet network with the wireless network, add the built-in ethernet interface (eth0) as bridge member with the following file:

```
sudo nano /etc/systemd/network/br0-member-eth0.network

[Match]
Name=eth0

[Network]
Bridge=br0
```

*Note* The access point software will add the wireless interface wlan0 to the bridge when the service starts. There is no need to create a file for the wireless interface.

### Configure DHCP networking (dhcpcd)

Network interfaces that are members of a bridge device are never assigned an IP address, as they communicate directly through the bridge. The bridge device itself needs an IP address in order to belong to the network.

Dhcpcd, the DHCP client on the Raspberry Pi, automatically requests an IP address for every active interface. So we need to block the `eth0` and `wlan0` interfaces from being processed, and let dhcpcd only configure `br0`.

```
sudo nano /etc/dhcpcd.conf
```

Add `denyinterfaces wlan0 eth0` near the beginning of the file (above the first `interface` line, if any). Interface `br0` will be configured as per dhcpcd's defaults, no specific entry is necessary.
Save the file to complete the IP configuration of the machine.

## Configure the access point software (hostapd)

Edit the hostapd configuration file, located at /etc/hostapd/hostapd.conf, to add the various parameters for your wireless network. After initial install, this will be a new/empty file.

```
sudo nano /etc/hostapd/hostapd.conf
```

Add the information below to the configuration file. This configuration assumes we are using channel 7, with a network name of NameOfNetwork, and a password AardvarkBadgerHedgehog. Note that the name and password should **not** have quotes around them. The passphrase should be between 8 and 64 characters in length.

To use the 5 GHz band, you can change the operations mode from hw_mode=g to hw_mode=a. Possible values for hw_mode are:
 - a = IEEE 802.11a (5 GHz)
 - b = IEEE 802.11b (2.4 GHz)
 - g = IEEE 802.11g (2.4 GHz)
 - ad = IEEE 802.11ad (60 GHz)

Note the lines `interface=wlan0` and `bridge=br0`: this directs hostapd to add the `wlan0` interface as bridge member to `br0` when the access point starts, completing the bridge.

```
interface=wlan0
bridge=br0
driver=nl80211
ssid=NameOfNetwork
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=AardvarkBadgerHedgehog
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

We now need to tell the system where to find this configuration file.

```
sudo nano /etc/default/hostapd
```

Find the line with #DAEMON_CONF, and replace it with this:

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

## Test your new wireless access point

We will proceed in two steps, first testing the network configuration and then the access point configuration. In case of error, verify your configuration and retry the current step. Do not advance to the next step.

### Step 1: Load the new network configuration
FIXME
Stop the DHCP client, releasing the network interfaces from their configuration:

```
sudo systemctl stop dhcpcd
```
Restart systemd-networkd, loading and configuring the network bridge:

```
sudo systemctl restart systemd-networkd
```
Start the DHCP client, so that the new `br0` interface acquires an IP address:

```
sudo systemctl start dhcpcd
```
Verify you have again access to the local network and the Internet from your Raspberry Pi before going to the next step.

### Step 2: Start the wireless access point service

Enable and start `hostapd`:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```
Using a wireless device, search for networks. The network SSID you specified in the hostapd configuration should now be present, and it should be accessible with the specified password.
Verify you have access to the local network and the Internet from your wireless device before completing the test.

## Verify the service starts at boot
To conclude the installation, restart your Raspberry Pi and verify the wireless access point becomes automatically available.
```
sudo systemctl reboot
```
