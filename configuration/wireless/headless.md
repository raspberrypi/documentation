# Setting up a Raspberry Pi headless

If you do not use a monitor or keyboard to run your Pi (known as headless), but you still need to do some wireless setup, there is a facility to enable wireless networking and SSH when creating a image.

Once an image is created on an SD card, by inserting it into a card reader on a Linux or Windows machines the boot folder can be accessed. Adding certain files to this folder will activate certain setup features on the first boot of the Pi itself. 

## Setting up wireless networking

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file in the boot folder, and when the Pi first boots, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking.

`wpa_supplicant.conf` file example:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

Note that some older wireless dongles don't support 5GHz networks.

More information on the `wpa_supplicant.conf` file can be found [here](wireless-cli.md). See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of 2 letter ISO 3166-1 country codes.

## Remote Access

With no keyboard or monitor, you will need some way of accessing the headless Raspberry Pi. There are a number of ways of doing this, and details can be found [here](../../remote-access/README.md).

