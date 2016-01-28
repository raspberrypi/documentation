## Connecting to a Pi over VNC using Mac OS

For Mac OS you will not need any extra software. Just select ``Go -> Connect to server ...`` (&#8984; K) from the Finder menu, enter ``vnc://raspberrypi.local:1`` as the Server Address and click ``Connect``. Here ``:1`` must correspond to the display on which you started the VNC server on your Pi. If there is a problem, try replacing ``raspberrypi.local`` with the IP address of your Pi.

Alternatively, you can use a program called RealVNC which is known to work with the Raspberry Pi VNC server; it can be downloaded from [realvnc.com](http://www.realvnc.com/download/vnc/latest).

Download the package file and open it. During the setup you'll be offered a choice of installation type. You only need the VNC viewer on your Mac, not the server, so select Custom and then *uncheck* VNC Server (see below).

![VNC OSX installation](images/osx/vnc-osx-install.png)

Click `Continue` and go ahead with the rest of the installation. Once the installation is complete, open Finder then select Applications on the left and enter VNC into the search box. VNC Viewer should then be shown. You might wish to create a shortcut to it in your Dock for future use.

![VNC connection dialogue](images/osx/vnc-osx-connect.png)

When you run it you'll be presented with the dialogue above. You will need to enter the IP address of the Raspberry Pi followed by the screen number (:0 or :1), for example 192.168.0.165:1

Click the Connect button and you'll be given an unencrypted connection warning.

![Unencrypted connection warning](images/osx/vnc-osx-warning.png)

Generally speaking, this warning is only applicable if the connection between your Mac and the Pi is going over the internet. If you're using a Local Area Network or a school network, then you can disregard this warning. Click *Continue* and you'll be prompted for the password that was specified when configuring the VNC server on the Raspberry Pi earlier. You should then find yourself at the Raspberry Pi desktop.

![Raspberry Pi desktop](images/osx/vnc-osx-connected.png)

Don't use the *logout* menu as you would on the Raspberry Pi desktop when you want to close down. Just close the RealVNC window itself and then use the kill command on the Raspberry Pi, described above, to shut down the VNC server.

For further documentation on RealVNC please visit this page: http://www.realvnc.com/products/vnc/documentation/latest/
