# Connecting to a Pi over VNC using Windows

On Windows you'll need to download and install a VNC client program. A commonly used one is TightVNC which can be downloaded from [tightvnc.com](http://www.tightvnc.com/download.php)

Choose either the 32 or 64 bit download depending on which version of Windows you are using. If you don't know then check by looking at System in Control Panel. Download the installer file and run it.

During installation you'll be offered the choice of Typical, Custom or Complete. You only need the VNC client and not the server, so choose Custom. Then select `TightVNC Server` and choose `Entire feature will be unavailable`. Click `Next`. Uncheck the option about Windows Firewall and click `Next` again, then `Install`.

![TightVNC Windows installation](images/win/vnc-win-install.png)

Once the installation is complete you should find `TightVNC Viewer` under the start menu. When you run it you'll be presented with the dialog below. You will need to enter the IP address of the Raspberry Pi followed by the screen number (`:0` or `:1`). For example: `192.168.0.6:1`

![TightVNC connection dialog](images/win/vnc-win-connect.png)

Click the `Connect` button and you will be prompted for the password that was specified when configuring the VNC server on the Raspberry Pi earlier. You should then find yourself at the Raspberry Pi desktop.

![Raspberry Pi desktop](images/win/vnc-win-connected.png)

Don't use the `logout` menu as you would on the Raspberry Pi desktop when you want to close down. Just close the TightVNC window itself and then use the kill command on the Raspberry Pi, described above, to shut down the VNC server.

For further documentation about TightVNC Viewer please visit [tightvnc.com](http://www.tightvnc.com/docs.php)
