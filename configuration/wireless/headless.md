# Setting up a Raspberry Pi headless

If you do not use a monitor or keyboard to run your Pi (known as headless), but you still need to do some wireless setup, there is a facility to enable wireless networking and SSH when creating a image.

Once an image is created on an SD card, by inserting it into a card reader on a Linux or Windows machines the boot folder can be accessed. Adding certain files to this folder will activate certain setup features on the first boot of the Pi itself. 

## Setting up wireless networking

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file in the boot folder, and when the Pi first boots, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking.

`wpa_supplicant.conf` file example:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert country code here>

network={
 ssid="<Name of your WiFi>"
 psk="<Password for your WiFi>"
}
```

Note that some older WiFi dongles don't support 5GHz networks.

More information on the `wpa_supplicant.conf` file can be found [here](wireless-cli.md). See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of country codes.

## Enabling SSH

SSH can be enabled by placing a file called `ssh` in to the boot folder. This flags the Pi to enable the SSH system on the next boot.

See [here](../../remote-access/ssh/README.md#3-enable-ssh-on-a-headless-raspberry-pi-add-file-to-sd-card-on-another-machine) for more details.

