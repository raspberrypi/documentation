# Setting WiFi up via the command line


This method is suitable if you don't have access to the graphical user interface normally used to set up WiFi on the Raspberry Pi. It's especially suitable for use with a serial console cable if you don't have access to a screen or wired Ethernet network. Note also that no additional software is required; everything you need is already included on the Raspberry Pi.   

## Getting WiFi network details  

To scan for WiFi networks, use the command `sudo iwlist wlan0 scan`. This will list all available WiFi networks, along with other useful information. Look out for:

1. `ESSID:"testing"`. This is the name of the WiFi network.   

1. `IE: IEEE 802.11i/WPA2 Version 1`. This is the authentication used; in this case it's WPA2, the newer and more secure wireless standard which replaces WPA. This guide should work for WPA or WPA2, but may not work for WPA2 enterprise; for WEP hex keys, see the last example [here](http://www.freebsd.org/cgi/man.cgi?query=wpa_supplicant.conf&sektion=5&apropos=0&manpath=NetBSD+6.1.5). You'll also need the password for the WiFi network. For most home routers this is located on a sticker on the back of the router. The ESSID (ssid) for the network in this case is `testing` and the password (psk) is `testingPassword`.

## Adding the network details to the Raspberry Pi
   
Open the `wpa-supplicant` configuration file in nano:

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`  

At the top of the file make sure that `update_config=1` is on a new line

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
```

Go to the bottom of the file and add the following:   

```
network={
    ssid="The_ESSID_from_earlier"
    psk="Your_wifi_password"
}
```

In the case of the example network, we would enter:  

```
network={
    ssid="testing"
    psk="testingPassword"
}
```
   
Now save the file by pressing **Ctrl+X** then **Y**, then finally press **Enter**.  

You can verify that the configuration file `wpa_supplicant.conf` works by using the command:

```
sudo wpa_supplicant -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf -d
```

At this point, `wpa-supplicant` will normally notice a change has occurred within a few seconds, and it will try and connect to the network. If it does not, either manually restart the interface with `sudo ifdown wlan0` and `sudo ifup wlan0`, or reboot your Raspberry Pi with `sudo reboot`.   

You can verify if it has successfully connected using `ifconfig wlan0`. If the `inet addr` field has an address beside it, the Pi has connected to the network. If not, check your password and ESSID are correct.   
