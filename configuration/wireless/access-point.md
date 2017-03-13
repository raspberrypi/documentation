##Setting up a Raspberry Pi as an access point

The Raspberry Pi can be used as a wireless access point, either by using the inbuilt wireless features of the Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wiress dongle that supprts access points.

In order to work as an access point, the Raspberry Pi will need to have access point software installed, along with a DHCP server software, to provide connecting devices with a network address.

Install all the requried software in one go with

```
sudo apt-get install dnsmasq hostapd
```

### Configuring the DHCP server (dnsmasq)



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

