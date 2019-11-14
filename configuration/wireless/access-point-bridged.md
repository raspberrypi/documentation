
# Setting up a Raspberry Pi as a Bridged Wireless Access Point

The Raspberry Pi can be used as a bridged wireless access point within an existing ethernet network. This will extend the network to wireless computers and devices.

If you wish to create a wireless network that could function stand-alone, consider instead setting up a [routed access point.](./access-point-routed.md)

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

This can be done using the inbuilt wireless features of the Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access point mode.
It is possible that some USB dongles may need slight changes to their settings. If you are having trouble with a USB wireless dongle, please check the forums.

This documentation was tested on a Raspberry Pi 3B running a factory installation of Raspbian Buster Lite (Jul. 2019). 

<a name="intro"></a>
## Before you start

* Ensure you have administrative access to your Raspberry Pi. The network setup will be entirely reset as part of the installation: local access, with screen and keyboard connected to your Raspberry Pi, is recommended.

  **Note:** If installing remotely through SSH,
    * Connect to your Raspberry Pi *by name*, e.g. `ssh pi@raspberrypi.local`. The IP address of your Raspberry Pi on the network *will probably change* after installation.
    * Be ready to add screen and keyboard in case you lose contact with your Raspberry Pi after installation. 
* Connect your Raspberry Pi to the ethernet network and boot the Raspbian OS.
* Ensure the Raspbian OS on your Raspberry Pi is [up to date](../../raspbian/updating.md) and reboot if packages were installed in the process.
* Have a wireless client (laptop, smartphone, ...) ready to test your new access point.

<a name="software-install"></a>
## Install the access point software

In order to work as a bridged access point, the Raspberry Pi needs to have the `hostapd` access point software package installed:

```
sudo apt install hostapd
```
Enable the wireless access point service to start when your Raspberry Pi boots:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

Software installation is complete. We will configure the access point software later on.

<a name="bridging"></a>
## Setup the network bridge

A bridge network device in the Raspberry Pi will join the ethernet and wireless networks using its built-in interfaces.

### Create a bridge device and populate the bridge

Add a bridge network device named `br0` by creating the following file:

```
sudo nano /etc/systemd/network/bridge-br0.netdev

[NetDev]
Name=br0
Kind=bridge
```

In order to bridge the ethernet network with the wireless network, first add the built-in ethernet interface (`eth0`) as bridge member with the following file:

```
sudo nano /etc/systemd/network/br0-member-eth0.network

[Match]
Name=eth0

[Network]
Bridge=br0
```

*Note:* The access point software will add the wireless interface `wlan0` to the bridge when the service starts. There is no need to create a file for that interface. This situation is particular to WiFi network interfaces.

Now enable the `systemd-networkd` service to create and populate the bridge when your Raspberry Pi boots:

```
sudo systemctl enable systemd-networkd
```

### Define the bridge device IP configuration

Network interfaces that are members of a bridge device are never assigned an IP address, since they communicate via the bridge. The bridge device itself needs an IP address, so that you can reach your Raspberry Pi on the network.

`dhcpcd`, the DHCP client on the Raspberry Pi, automatically requests an IP address for every active interface. So we need to block the `eth0` and `wlan0` interfaces from being processed, and let `dhcpcd` only configure `br0` via DHCP.

```
sudo nano /etc/dhcpcd.conf
```

Add the following line near the beginning of the file (above the first `interface xxx` line, if any):
```
denyinterfaces wlan0 eth0
```
Interface `br0` will be configured as per defaults via DHCP, no specific entry is necessary. Save the file to complete the IP configuration of the machine.

<a name="ap-config"></a>
## Configure the access point software

Create the `hostapd` configuration file, located at `/etc/hostapd/hostapd.conf`, to add the various parameters for your wireless network. 

```
sudo nano /etc/hostapd/hostapd.conf
```

Add the information below to the configuration file. This configuration assumes we are using channel 7, with a network name of `NameOfNetwork`, and a password `AardvarkBadgerHedgehog`. Note that the name and password should **not** have quotes around them. The passphrase should be between 8 and 64 characters in length.

To use the 5 GHz band, you can change the operations mode from `hw_mode=g` to `hw_mode=a`. Possible values for `hw_mode` are:
 - a = IEEE 802.11a (5 GHz)
 - b = IEEE 802.11b (2.4 GHz)
 - g = IEEE 802.11g (2.4 GHz)
 - ad = IEEE 802.11ad (60 GHz)

```
interface=wlan0
bridge=br0
ssid=NameOfNetwork
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=AardvarkBadgerHedgehog
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```
Note the lines `interface=wlan0` and `bridge=br0`: these direct `hostapd` to add the `wlan0` interface as bridge member to `br0` when the access point starts, completing the bridge between ethernet and wireless.

<a name="conclusion"></a>
## Run your new wireless access point

It is now time restart your Raspberry Pi and verify the wireless access point becomes automatically available.

```
sudo systemctl reboot
```
Once your Raspberry Pi has restarted, search for WiFi networks with your wireless client. The network SSID you specified in file `/etc/hostapd/hostapd.conf` should now be present, and it should be accessible with the specified password.

If your wireless client has access to the local network and the Internet, congratulations on your new access point!

If you encounter difficulties, contact the forums for assistance. Please refer to this page in your message.
