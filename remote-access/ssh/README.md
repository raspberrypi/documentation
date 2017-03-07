# SSH (Secure Shell)

You can access the command line of a Raspberry Pi remotely from another computer or device on the same network using SSH.

##1. Set up your client

SSH is built into Linux distributions and Mac OS. For Windows and mobile devices, third-party SSH clients are available. See the following guides for using SSH with the OS on your computer or device:

- [Linux & Mac OS](unix.md)
- [Windows](windows.md)
- [iOS](ios.md)
- [Android](android.md)

Note that you only have access to the command line, not the full desktop environment. For the full remote desktop, see [VNC](../vnc/README.md).

##2. Set up your local network and wireless connectivity

Make sure your Raspberry Pi is properly set up and connected. If you are using [wireless connectivity](../../configuration/wireless/wireless-cli.md), use the `wpa_supplicant.conf` config file. 

If you are not using wireless connectivity, plug your Raspberry Pi directly into the router.

##3. Enable SSH
As of the November 2016 release, Raspbian has the SSH server disabled by default. It can be enabled manually from the desktop:

1. Launch `Raspberry Pi Configuration` from the `Preferences` menu
1. Navigate to the `Interfaces` tab
1. Select `Enabled` next to `SSH`
1. Click `OK`

Alternatively, [raspi-config](../../configuration/raspi-config.md) can be used:

1. Enter `sudo raspi-config` in a terminal window
1. Select `Interfacing Options`
1. Navigate to and select `SSH`
1. Choose `Yes` 
1. Select `Ok`
1. Choose `Finish`

For headless setup, SSH can be enabled by placing a file named 'ssh', without any extension, onto the boot partition of the SD card. When the Pi boots, it looks for the 'ssh' file. If it is found, SSH is enabled, and the file is deleted. The content of the file does not matter: it could contain text, or nothing at all.
