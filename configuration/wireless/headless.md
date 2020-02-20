# Setting up a Raspberry Pi headless

If you do not use a monitor or keyboard to run your Pi (known as headless), but you still need to do some wireless setup, there is a facility to enable wireless networking and SSH when creating a image.

Once an image is created on an SD card, by inserting it into a card reader on a Linux or Windows machines the boot folder can be accessed. Adding certain files to this folder will activate certain setup features on the first boot of the Pi itself. 

## Setting up wireless networking

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file in the boot folder, and when the Pi first boots, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking.

You can use notepad++ so that the file is saved in correct formats. You can go in edit--> EOL Conversion--> UNIX so that Raspbian understands the code properly.Paste the below After that and save it.

`wpa_supplicant.conf` file example:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert country code here>

network={
 scan_ssid=1
 ssid="<Name of your WiFi>"
 psk="<Password for your WiFi>"
}
```

Note that some older WiFi dongles don't support 5GHz networks.

More information on the `wpa_supplicant.conf` file can be found [here](wireless-cli.md). See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of country codes.

## Enabling SSH

SSH can be enabled by placing a file called `ssh` in to the boot folder. This flags the Pi to enable the SSH system on the next boot.

See [here](../../remote-access/ssh/README.md#3-enable-ssh-on-a-headless-raspberry-pi-add-file-to-sd-card-on-another-machine) for more details.

## Enabling VNC
Once the SSH and wpa_supplicant files are in place you will need do download putty in your PC and first you will also need to identify the IP of your device via router stats or if its connected to a phone you can directly check its IP. 

After getting the IP you need to enable Real VNC. For that download Putty and put the IP of your Raspberry Pi and click on ssh and click open. Now your device is connected via SSH. Now you need to configure it inorder to see its screen on your device.

When asked for user ID and Password type user ID : pi pswd:raspberry (If you have changed it to something else type that)
Now type 
sudo raspi-config

Now the Configuration menu will open now go to Interfacing options--> RealVNC--> Enable
Restart your PI after it.

Now just put the IP of your raspberry Pi on your VNC viewer and you're good to go.

If you want to play games don't forget to enable direct capture in VNC settings otherwise it will not show you the app on the screen.
