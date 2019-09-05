
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

* Ensure you have administrative access to your Raspberry Pi. The network setup will be entirely reset as part of the installation, so local access, with screen and keyboard connected to your Raspberry Pi is recommended.

  **Note:** If installing remotely through SSH,
    * Connect to your Raspberry Pi by name, e.g. `ssh pi@raspberrypi.local`. The IP address of your Raspberry Pi on the network might change after installation.
    * Be ready to add screen and keyboard in case you lose contact with your Raspberry Pi after the installation. 
* Connect your Raspberry Pi to the ethernet network and boot the Raspbian OS.
* Ensure the Raspbian OS on your Raspberry Pi is [up to date](../../raspbian/updating.md) and reboot if packages were installed in the process.
* Have a wireless client (laptop, smartphone, ...) ready to test your new access point.

<a name="hostapd-install"></a>
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

Software installation is complete. We will configure the access point software later on.

<a name="bridging"></a>
## Setup the network bridge

### Create a bridge device and populate the bridge (systemd-networkd)

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

**Note:** The access point software will add the wireless interface `wlan0` to the bridge when the service starts. There is no need to create a file for that interface. This situation is particular to WiFi network interfaces.

Enable the `systemd-networkd` service to create and populate the bridge when your Raspberry Pi boots:

```
sudo systemctl enable systemd-networkd
```

### Configure DHCP networking (dhcpcd)

Network interfaces that are members of a bridge device are never assigned an IP address, since they communicate via the bridge. The bridge device itself now needs an IP address, so that you can reach your Raspberry Pi on the network.

`dhcpcd`, the DHCP client on the Raspberry Pi, automatically requests an IP address for every active interface. So we need to block the `eth0` and `wlan0` interfaces from being processed, and let `dhcpcd` only configure `br0`.

```
sudo nano /etc/dhcpcd.conf
```

Add `denyinterfaces wlan0 eth0` near the beginning of the file (above the first `interface` line, if any). Interface `br0` will be configured as per defaults, no specific entry is necessary. Save the file to complete the IP configuration of the machine.

<a name="hostapd-config"></a>
## Configure the access point software (hostapd)

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

Note the lines `interface=wlan0` and `bridge=br0`: this directs `hostapd` to add the `wlan0` interface as bridge member to `br0` when the access point starts, completing the bridge.

```
interface=wlan0
bridge=br0
#driver=nl80211
ssid=NameOfNetwork
hw_mode=g
channel=7
#wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=AardvarkBadgerHedgehog
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```
## Run your new wireless access point

It is now time restart your Raspberry Pi and verify the wireless access point becomes automatically available.

```
sudo systemctl reboot
```
Once your Raspberry Pi has restarted, search for WiFi networks with a wireless device. The network SSID you specified in file `/etc/hostapd/hostapd.conf` should now be present, and it should be accessible with the specified password.

If you have access to the local network and the Internet from your wireless device, congratulations on your new access point!

If you encounter difficulties, read these troubleshooting tips and verify your configuration:
* *Step 1:* From a computer on the network, does `ping raspberrypi.local` work, and shows an IP address that belongs to the same network as the computer, for example `192.168.1.2`?
    * If ping fails or the address looks different, like `169.254.x.x`, verify [bridge networking setup](#bridging) (`systemd-networkd` and `dhcpcd`)
    * If ping succeeds, on to Step 2
* *Step 2:* From your test wireless device, do you see the WiFi network name and can successfuly authenticate using the password defined in file `/etc/hostapd/hostapd.conf`?
    * If the wireless device cannot find the network or authentication fails, verify access point software [installation](#hostapd-install) and [configuration.](#hostapd-config)
    * If connecting to the wireless network succeeds, but the device cannot reach machines on the network or the Internet, verify that the DHCP server on the network (often located in the router) answers to the IP address request coming from the wireless device.
    * If the wireless access point and the DHCP server seem ok, on to Step 3
* *Step 3:* Contact the forums for further assistance. Please add a link to this page in your message. 
If possible and reasonably convenient, copy-paste the following block of commands on your Raspberry Pi and include their output to your message on the forum:
```
# System identification
lsb_release -a
uname -a
# Services status
systemctl status hostapd
systemctl status dhcpcd
systemctl status systemd-networkd
```
