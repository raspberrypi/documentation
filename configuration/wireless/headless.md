# Setting up a Raspberry Pi Headless

If you do not have a monitor or keyboard (known as headless) but still need to do some wireless setup, there is facility to enable wireless networking and SSH when creating a image.

Once an image is created on an SD card (or similar), when inserted in to a reader on a Linux or Windows machines, the boot folder can be accessed. By adding certain files to this folder, on the first boot on the Pi itself, certain setup features can be activated. 

## Setting up Wireless Networking

You will need to define a wpa_supplicant.conf file for you particular wireless network. Put this file in the boot folder, and when the Pi first boots it will copy that file in to the correct location in the Linux root filesystem and use those settings to start up wireless networking.

More information on the wpa_supplicant.conf file can be found [here](wireless-cli.md)

## Enabling SSH

SSH can be enabled by placing a file called `ssh` in to the boot folder. This flags the Pi to enable the SSH system on the next boot.

See [here](https://github.com/raspberrypi/documentation/blob/master/remote-access/ssh/README.md#3-enable-ssh-on-a-headless-raspberry-pi-add-file-to-sd-card-on-another-machine) for more details.

