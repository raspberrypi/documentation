# Setting up a Raspberry Pi as a Routed Wireless Access Point

The Raspberry Pi can be used as a wireless access point routing to an existing ethernet network. This will create a new wireless network entirely managed by the Raspberry Pi.

If you wish to extend an existing ethernet network to wireless clients, consider instead setting up a [bridged access point.](./access-point-bridged.md)

```
                                         +- RPi -------+
                                     +---+ 10.10.0.2   |          +- Laptop ----+
                                     |   |     WiFi AP +-)))  (((-+ WiFi STA    |
                                     |   | 192.168.4.1 |          | 192.168.4.2 |
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
This can be done using the inbuilt wireless features of the Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access point mode.
It is possible that some USB dongles may need slight changes to their settings. If you are having trouble with a USB wireless dongle, please check the forums.

This documentation was tested on a Raspberry Pi 3B running a factory installation of Raspbian Buster Lite (July 2019). 

<a name="intro"></a>
## Before you start

* Ensure you have administrative access to your Raspberry Pi. The network setup will be modified as part of the installation: local access, with screen and keyboard connected to your Raspberry Pi, is recommended.
* Connect your Raspberry Pi to the ethernet network and boot the Raspbian OS.
* Ensure the Raspbian OS on your Raspberry Pi is [up to date](../../raspbian/updating.md) and reboot if packages were installed in the process.
* Take note of the IP configuration of the ethernet network the Raspberry Pi is connected to: 
    * In this document, we assume IP network `10.10.0.0/24` is configured on the ethernet LAN, and the Raspberry Pi is to manage IP network `192.168.4.0/24` for wireless clients.
    * Please select another IP network for wireless, e.g. `192.168.10.0/24`, in case IP network `192.168.4.0/24` is already in use by your ethernet LAN.
* Have a wireless client (laptop, smartphone, ...) ready to test your new access point.

<a name="software-install"></a>
## Install the access point and network management software

In order to work as an access point, the Raspberry Pi needs to have the `hostapd` access point software package installed:

```
sudo apt install hostapd
```
Enable the wireless access point service to start when your Raspberry Pi boots:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

In order to provide network management services (DNS, DHCP) to wireless clients, the Raspberry Pi needs to have the `dnsmasq` software package installed:

```
sudo apt install dnsmasq
```
Finally, install `netfilter-persistent` and its plugin `iptables-persistent`. This utilty helps saving firewall rules and restores them when the Raspberry Pi boots:

```
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
```
Software installation is complete. We will configure the software packages later on.

<a name="routing"></a>
## Setup the network router

The Raspberry Pi will run and manage a stand-alone wireless network. The Raspberry Pi will also route between wireless and ethernet networks, providing Internet access to wireless clients. At your option, you can skip routing and run the wireless network in complete isolation. 

### Define the wireless interface IP configuration

In this document, we assume IP network `10.10.0.0/24` is configured on the ethernet LAN, and the Raspberry Pi will manage IP network `192.168.4.0/24` for wireless clients.
*Note:* Please select another IP network for wireless, e.g. `192.168.10.0/24`, in case IP network `192.168.4.0/24` is already in use by your ethernet LAN.

The Raspberry Pi runs a DHCP server for the wireless network, this requires static IP configuration for the wireless interface (`wlan0`) in the Raspberry Pi. 
The Raspberry Pi acts as router on the wireless network, as customary we will give it the first IP address in the network: `192.168.4.1`.

To configure the static IP address, edit the configuration file for `dhcpcd` with:

```
sudo nano /etc/dhcpcd.conf
```

Go to the end of the file and add the following:

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

### Enable routing and IP masquerading

This section configures the Raspberry Pi to let wireless clients access computers on the main network, and from there the Internet.
*NOTE:* If you wish to block wireless clients from accessing the main network and the Internet, skip this section. 

To enable routing, i.e. allow traffic to flow from one network to an other in the Raspberry Pi, create the following file:
```
sudo nano /etc/sysctl.d/routed-ap.conf

# https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md
# Enable IPv4 routing
net.ipv4.ip_forward=1
```
Enabling routing will allow hosts from network `192.168.4.0/24` to reach the LAN and the main router towards the Internet. In order to allow traffic between clients on this foreign wireless network and the Internet without changing the configuration of the main router, the Raspberry Pi can substitute the IP address of wireless clients with its own IP address on the LAN using a "masquerade" firewall rule.
* The main router will see all outgoing traffic from wireless clients as coming from the Raspberry Pi, allowing communication with the Internet.
* The Raspberry Pi will receive all incoming traffic, substitute the IP addresses back and forward traffic to the origin wireless client.

This process is configured by adding a single firewall rule in the Raspberry Pi:

```
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```
Now save the current firewall rules for IPv4 (including the rule above) and IPv6 to be loaded at boot by the `netfilter-persistent` service:
```
sudo netfilter-persistent save
```
Filtering rules are saved to directory `/etc/iptables/`. If in the future you change the configuration of your firewall, make sure to save the configuration to files before rebooting.

### Configure the DHCP and DNS services for the wireless network

The DHCP and DNS services are provided by `dnsmasq`. The default configuration file serves as template for all possible configuration options, when we only need a few. It is easier to start from an empty file. 

Rename the default configuration file and edit a new one:

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
```
Add the following to the file and save it:

```
interface=wlan0 # Listening interface
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
                # Pool of IP addresses served via DHCP
domain=wlan     # Local wireless DNS domain
address=/gw.wlan/192.168.4.1
                # Alias for this router
```

The Raspberry Pi will deliver IP addresses between `192.168.4.2` and `192.168.4.20`, with a lease time of 24 hours, to wireless DHCP clients. You should be able to reach the Raspberry Pi under the name `gw.wlan` from wireless clients.

There are many more options for `dnsmasq`; see the default configuration file or the [online documentation](http://www.thekelleys.org.uk/dnsmasq/doc.html) for details.

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
<a name="conclusion"></a>
## Run your new wireless access point

It is now time restart your Raspberry Pi and verify the wireless access point becomes automatically available.

```
sudo systemctl reboot
```
Once your Raspberry Pi has restarted, search for WiFi networks with your wireless client. The network SSID you specified in file `/etc/hostapd/hostapd.conf` should now be present, and it should be accessible with the specified password.

If SSH is enabled on the Raspberry Pi, it should be possible to connect to from your wireless client as follows, assuming the `pi` account is present: `ssh pi@192.168.4.1` or `ssh pi@gw.wlan`

If your wireless client has access to your Raspberry Pi (and the Internet), congratulations on your new access point!

If you encounter difficulties, contact the forums for assistance. Please refer to this page in your message.
