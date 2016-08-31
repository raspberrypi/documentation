# SSH (Secure Shell)

You can access the command line of a Raspberry Pi remotely from another computer or device on the same network using `ssh`.

##1. Set up your client
SSH is built into Linux distributions and Mac OS. For Windows and mobile devices, third-party SSH clients are available. See the following guides for using SSH depending on the OS used by the computer or device you are connecting from:

- [Linux & Mac OS](unix.md)
- [Windows](windows.md)
- [iOS](ios.md)
- [Android](android.md)

Note you only have access to the command line, not the full desktop environment. For full remote desktop see [VNC](../vnc/README.md).

##2. Set up your local network and WiFi
Make sure your Raspberry Pi is properly set up and connected. If you're using [WiFi](../../configuration/wireless/wireless-cli.md), this is done using the `wpa_supplicant.conf` config file. 

Otherwise, plug your Raspberry Pi directly into the router.

##3. Enable SSH
The Raspberry Pi has an SSH server enabled by default. The SSH server on your Raspberry Pi may be disabled, in which case you will have to enable it manually. This is done using [raspi-config](../../configuration/raspi-config.md):

Enter `sudo raspi-config` in the terminal, then navigate to `ssh`, hit `Enter` and select `Enable or disable ssh server`.


