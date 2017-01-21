# SSH (Secure Shell)

You can access the command line of a Raspberry Pi remotely from another computer or device on the same network using SSH.

##1. Set up your client
SSH is built into Linux distributions and Mac OS. For Windows and mobile devices, third-party SSH clients are available. See the following guides for using SSH depending on the OS used by the computer or device you are connecting from:

- [Linux & Mac OS](unix.md)
- [Windows](windows.md)
- [iOS](ios.md)
- [Android](android.md)

Note that you only have access to the command line, not the full desktop environment. For the full remote desktop, see [VNC](../vnc/README.md).

##2. Set up your local network and WiFi
Make sure your Raspberry Pi is properly set up and connected. If you're using [WiFi](../../configuration/wireless/wireless-cli.md), this is done using the `wpa_supplicant.conf` config file. 

Otherwise, plug your Raspberry Pi directly into the router.

##3. Enable SSH
As of the November 2016 release, Raspbian has the SSH server disabled by default. You will have to enable it manually. This is done using [raspi-config](../../configuration/raspi-config.md):

1. Enter `sudo raspi-config` in the terminal
2. Select `Advanced options`
3. Navigate to and select `SSH`
4. Choose `Yes` 
5. Select `Ok`
6. Choose `Finish`

For headless setup, SSH can be enabled by placing a file named 'ssh', without any extension, onto the boot partition of the SD card. When the Pi boots, it looks for the 'ssh' file; if it is found, SSH is enabled and then the file is deleted. The content of the file doesn't matter: it could contain any text or nothing at all.
