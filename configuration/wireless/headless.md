# Setting up a Raspberry Pi headless

If you do not use a monitor or keyboard to run your Pi (known as headless), but you still need to do some wireless setup, there is a facility to enable wireless networking and SSH when creating a image.

Once an image is created on an SD card, by inserting it into a card reader on a Linux or Windows machines the [boot folder](../boot_folder.md) can be accessed. Adding certain files to this folder will activate certain setup features on the first boot of the Pi itself. 

## Setting up wireless networking

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file onto the boot partition of the SD card, and when the Pi first boots, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking. **After the Pi is connected to power, make sure to wait a few (up to 5) minutes for it to boot up and register on the network.** The Pi's IP address will not be visible immediately after power on, so this step is crucial to connect to it headlessly. Depending on the OS and editor you are creating this on, the file could have incorrect newlines or the wrong file extension so make sure you use an editor that accounts for this. Linux expects the line feed (LF) newline character. For more information, see this [Wikipedia article](https://en.wikipedia.org/wiki/Newline). 

`wpa_supplicant.conf` file example:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=<Insert 2 letter ISO 3166-1 country code here>
update_config=1

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

Where the country code should be set the two letter ISO/IEC alpha2 code for the country in which you are using, e.g.

* GB (United Kingdom)
* FR (France)
* DE (Germany)
* US (United States)
* SE (Sweden)

Here is a more elaborate example that should work for most typical wpa2 personal networks. This template below works for 2.4ghz/5ghz hidden or not networks. The utilization of quotes around the ssid - psk can help avoid any oddities if your network ssid or password has special chars (! @ # $ etc)

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
        scan_ssid=1
        ssid="<Name of your wireless LAN>"
        psk="<Password for your wireless LAN>"
        proto=RSN
        key_mgmt=WPA-PSK
        pairwise=CCMP
        auth_alg=OPEN
}
```

Note that some older pi's (zerow or 3b) or usb wireless dongles don't support 5GHz networks.

More information on the `wpa_supplicant.conf` file can be found [here](wireless-cli.md). See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of 2 letter ISO 3166-1 country codes.

## Remote Access

With no keyboard or monitor, you will need some way of accessing the headless Raspberry Pi. There are a number of ways of doing this, and details can be found [here](../../remote-access/README.md).

