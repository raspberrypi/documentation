##Setting up a Raspberry Pi as an access point

The Raspberry Pi can be used as a wireless access point, either by using the inbuilt wireless features of the Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access points.

In order to work as an access point, the Raspberry Pi will need to have access point software installed, along with a DHCP server software, to provide connecting devices with a network address.

Install all the required software in one go with

```
sudo apt-get install dnsmasq hostapd
```

## Configuring a static IP

To act as a server we need the server to have a static IP address. This documentation assumes we are using the standard 192.168.x.x IP address for our wireless network, so we will assign the server the IP address 192.168.0.1

Firstly the standard interface handling for wlan0 needs to be disabled. Normally the dhcpd daemon will search the network for another DHCP server to assign a IP address to wlan0, this is disabled by editing the configuration file
```
nano /etc/dhcp.conf
```
Add `denyinterfaces wlan0` to the end of the file but above any other added `interface` lines and save the file.

To configure the static IP address, edit the interfaces configuration file with 
```
sudo nano /etc/netowrk/interfaces
```
Find the wlan0 section and edit it so its looks like the following.
```
allow-hotplug wlan0  
iface wlan0 inet static  
    address 192.168.0.1
    netmask 255.255.255.0
    network 192.168.0.0
```

Now restart the DHCP daemon and set up the new wlan0 configuration

```
sudo service dhcpd restart
sudo ifdown wlan0
sudo ifup wlan0
```

### Configuring the DHCP server (dnsmasq)

dnsmasq provides the needed DHCP service. By default the configuration file contains a lot of information that is not needed, and it is easier to start from scratch, so firstly rename this configuration file, and edit a new one.
```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  
sudo nano /etc/dnsmasq.conf
```
Type or copy the following information into the dnsmasq configuration file.
```
interface=wlan0      # Use the require wireless interface - usually wlan0
  dhcp-range=192.168.0.2,192.168.0.20,255.255.255.0, 24h
```
So for wlan0 we are going to provide IP addresses between 192.168.0.2 and 192.168.0.20, with a lease time of 24 hours. If you are providing DHCP services for other network devices (e.g. eth0), you could add more sections with the appropriate interface header, with the range of addresses you intend to provide to that interface.

dnsmasq has many more options, see the dnsmasq documentation for more details.

### Configuring the Access Point host software (hostapd)

You need to edit the hostapd configuration file, located at /etc/hostapd/hostapd.conf, to add the various parameters for your wireless network. After initial install, this will be a new/empty file.

```
sudo nano /etc/hostapd/hostapd.confg
```
Add the following information to the configuration file, editing in the appropriate entry for options inside <...>
```
interface=<Usually wlan0, but check ifconfig to determine the name of the wireless device to use>
driver=nl80211
ssid=<name of you wireless network here>
hw_mode=g
channel=<required channel number, between 1 and 13>
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=<your wireless network password>
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

We now need to tell the system where to find this configuration file.
```
sudo nano /etc/default/hostapd
```
Find the line with #DAEMON_CONF, and repalce with
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

## Start it up

Now start up the remaining services
```
sudo service hostapd start  
sudo service dnsmasq start  
```

Using a wireless device, search for networks, and the network SSID you specified in the hostapd configuration should now be present, and accessible with the specified password.

If SSH is enabled on the Raspberry Pi access point it should be possible to connect to it from another Linux box (or system with SSH connectivity present) as follows, assuming the `pi` account is present.
```
ssh pi@192.168.0.1
```




