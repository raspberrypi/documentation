
# Setting up a Raspberry Pi as a bridged wireless access point

The Raspberry Pi can be used as a bridged wireless access point within an existing Ethernet network. This will extend the network to wireless computers and devices.

If you wish to create a standalone wireless network, consider instead setting up a [routed access point](./access-point-routed.md).

```
                                         +- RPi -------+
                                     +---+ 10.10.0.2   |          +- Laptop ----+
                                     |   |     WLAN AP +-)))  (((-+ WLAN Client |
                                     |   |  Bridge     |          | 10.10.0.5   |
                                     |   +-------------+          +-------------+
                 +- Router ----+     |
                 | Firewall    |     |   +- PC#2 ------+
(Internet)---WAN-+ DHCP server +-LAN-+---+ 10.10.0.3   |
                 |   10.10.0.1 |     |   +-------------+
                 +-------------+     |
                                     |   +- PC#1 ------+
                                     +---+ 10.10.0.4   |
                                         +-------------+
```

A bridged wireless access point can be created using the inbuilt wireless features of the Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access point mode.
It is possible that some USB dongles may need slight changes to their settings. If you are having trouble with a USB wireless dongle, please check the [forums](https://www.raspberrypi.org/forums/).

This documentation was tested on a Raspberry Pi 3B running a fresh installation of Raspberry Pi OS Buster.

<a name="intro"></a>
## Before you start

* Ensure you have administrative access to your Raspberry Pi. The network setup will be entirely reset as part of the installation: local access, with screen and keyboard connected to your Raspberry Pi, is recommended.

  **Note:** If installing remotely via SSH,
    * Connect to your Raspberry Pi **by name**, e.g. `ssh pi@raspberrypi.local`. The IP address of your Raspberry Pi on the network **will probably change** after installation.
    * Be ready to add screen and keyboard in case you lose contact with your Raspberry Pi after installation.
* Connect your Raspberry Pi to the Ethernet network and boot the Raspberry Pi OS.
* Ensure the Raspberry Pi OS on your Raspberry Pi is [up-to-date](../../raspbian/updating.md) and reboot if packages were installed in the process.
* Have a wireless client (laptop, smartphone, ...) ready to test your new access point.

<a name="software-install"></a>
## Install the access point software

In order to work as a bridged access point, the Raspberry Pi needs to have the `hostapd` access point software package installed:

```
sudo apt install hostapd
```
Enable the wireless access point service and set it to start when your Raspberry Pi boots:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

Software installation is complete. We will configure the access point software later on.

<a name="bridging"></a>
## Setup the network bridge

A bridge network device running on the Raspberry Pi will connect the Ethernet and wireless networks using its built-in interfaces.

### Create a bridge device and populate the bridge

Add a bridge network device named `br0` by creating a file using the following command, with the contents below:

```
sudo nano /etc/systemd/network/bridge-br0.netdev
```

File contents:
```
[NetDev]
Name=br0
Kind=bridge
```

In order to bridge the Ethernet network with the wireless network, first add the built-in Ethernet interface (`eth0`) as a bridge member by creating the following file:

```
sudo nano /etc/systemd/network/br0-member-eth0.network
```

File contents:
```
[Match]
Name=eth0

[Network]
Bridge=br0
```

**Note:** The access point software will add the wireless interface `wlan0` to the bridge when the service starts. There is no need to create a file for that interface. This situation is particular to wireless LAN interfaces.

Now enable the `systemd-networkd` service to create and populate the bridge when your Raspberry Pi boots:

```
sudo systemctl enable systemd-networkd
```

### Define the bridge device IP configuration

Network interfaces that are members of a bridge device are never assigned an IP address, since they communicate via the bridge. The bridge device itself needs an IP address, so that you can reach your Raspberry Pi on the network.

`dhcpcd`, the DHCP client on the Raspberry Pi, automatically requests an IP address for every active interface. So we need to block the `eth0` and `wlan0` interfaces from being processed, and let `dhcpcd` configure only `br0` via DHCP.

```
sudo nano /etc/dhcpcd.conf
```

Add the following line near the beginning of the file (above the first `interface xxx` line, if any):
```
denyinterfaces wlan0 eth0
```
Go to the end of the file and add the following:

```

interface br0
```
With this line, interface `br0` will be configured in accordance with the defaults via DHCP. Save the file to complete the IP configuration of the machine.

<a name="wifi-cc-rfkill"></a>
## Ensure wireless operation

Countries around the world regulate the use of telecommunication radio frequency bands to ensure interference-free operation.
The Linux OS helps users [comply](https://wireless.wiki.kernel.org/en/developers/regulatory/statement) with these rules by allowing applications to be configured with a two-letter "WiFi country code", e.g. `US` for a computer used in the United States.

In the Raspberry Pi OS, 5 GHz wireless networking is disabled until a WiFi country code has been configured by the user, usually as part of the initial installation process (see wireless configuration pages in this [section](README.md) for details.)

To ensure WiFi radio is not blocked on your Raspberry Pi, execute the following command:

```
sudo rfkill unblock wlan
```

This setting will be automatically restored at boot time. We will define an appropriate country code in the access point software configuration, next.

<a name="ap-config"></a>
## Configure the access point software

Create the `hostapd` configuration file, located at `/etc/hostapd/hostapd.conf`, to add the various parameters for your new wireless network.

```
sudo nano /etc/hostapd/hostapd.conf
```

Add the information below to the configuration file. This configuration assumes we are using channel 7, with a network name of `NameOfNetwork`, and a password `AardvarkBadgerHedgehog`. Note that the name and password should **not** have quotes around them. The passphrase should be between 8 and 64 characters in length.

```
country_code=GB
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
Note the lines `interface=wlan0` and `bridge=br0`: these direct `hostapd` to add the `wlan0` interface as a bridge member to `br0` when the access point starts, completing the bridge between Ethernet and wireless.

Note the line `country_code=GB`: it configures the computer to use the correct wireless frequencies in the United Kingdom. **Adapt this line** and specify the two-letter ISO code of your country. See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of two-letter ISO 3166-1 country codes.

To use the 5 GHz band, you can change the operations mode from `hw_mode=g` to `hw_mode=a`. Possible values for `hw_mode` are:
 - a = IEEE 802.11a (5 GHz) (Raspberry Pi 3B+ onwards)
 - b = IEEE 802.11b (2.4 GHz)
 - g = IEEE 802.11g (2.4 GHz)

Note that when changing the `hw_mode`, you may need to also change the `channel` - see [Wikipedia](https://en.wikipedia.org/wiki/List_of_WLAN_channels) for a list of allowed combinations.

<a name="conclusion"></a>
## Run your new wireless access point

Now restart your Raspberry Pi and verify that the wireless access point becomes automatically available.

```
sudo systemctl reboot
```
Once your Raspberry Pi has restarted, search for wireless networks with your wireless client. The network SSID you specified in file `/etc/hostapd/hostapd.conf` should now be present, and it should be accessible with the specified password.

If your wireless client has access to the local network and the internet, congratulations on setting up your new access point!

If you encounter difficulties, contact the [forums](https://www.raspberrypi.org/forums/) for assistance. Please refer to this page in your message.
