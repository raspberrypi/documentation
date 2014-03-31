# VNC (Virtual Network Computing)

Sometimes it is not convenient to work directly on the Raspberry Pi. Maybe you would like to work on it but from another computer by remote control.

VNC is a graphical desktop sharing system that allows you to remotely control the desktop interface of one computer from another. It transmits the keyboard and mouse events from the controller and receives back updates to the screen over the network from the remote host.

You will see the desktop of the Raspberry Pi inside a window on your computer. You'll be able to control it as though you were working on the Raspberry Pi itself.

- On your Pi (using a monitor or via [SSH](../ssh/README.md)), install the TightVNC package:

```
sudo apt-get install tightvncserver
```

- Next Run TightVNC Server which will prompt you to enter a Password and an optional View Only Password

```
tightvncserver
```

- Start a VNC server from the shell prompt. This example starts a session on VNC display zero (```:0```) with full HD resolution:

```
vncserver :0 -geometry 1920x1080 -depth 24
```

- Now on your computer, install and run the VNC client:

  - On a Linux machine install the package `xtightvncviewer`

    e.g. `sudo apt-get install xtightvncviewer`

  - Otherwise, TightVNC is downloadable from [tightvnc.com](http://www.tightvnc.com/download.php)

### Automation and run at boot

You can create a simple file with the command to run the VNC server on the Pi, to save having to remember it:

- Create a file containing:

```
#!/bin/sh
vncserver :0 -geometry 1920x1080 -depth 24 -dpi 96
```

- Save this as ```vnc.sh``` (example)

- Make the file executable:

```
chmod +x vnc.sh
```

- Then run at any time with:

```
./vnc.sh
```

To run at boot:

- Log in to a root shell on the Pi:

```
sudo su
```

- Navigate to the directory ```/etc/init.d/```:

```
cd /etc/init.d/
```

- Create a new file here containing the following script:

```
### BEGIN INIT INFO
# Provides: vncboot
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start VNC Server at boot time
# Description: Start VNC Server at boot time.
### END INIT INFO

#! /bin/sh
# /etc/init.d/vncboot

USER=root
HOME=/root

export USER HOME

case "$1" in
 start)
  echo "Starting VNC Server"
  #Insert your favoured settings for a VNC session
  /usr/bin/vncserver :0 -geometry 1280x800 -depth 16 -pixelformat rgb565
  ;;

 stop)
  echo "Stopping VNC Server"
  /usr/bin/vncserver -kill :0
  ;;

 *)
  echo "Usage: /etc/init.d/vncboot {start|stop}"
  exit 1
  ;;
esac

exit 0
```

- Save this file as ```vncboot``` (example)

- Make this file executable:

```
chmod 755 vncboot
```

- Enable dependency based boot sequencing:

```
update-rc.d /etc/init.d/vncboot defaults
```

- If enabling dependency based boot sequencing was successful, it says:

```
update-rc.d: using dependency based boot sequencing
```

- But if it says:

```
update-rc.d: error: unable to read /etc/init.d//etc/init.d/vncboot
```

- then try the following command:

```
update-rc.d vncboot defaults
```

- Reboot your Raspberry Pi and you should find a vncserver already started

You'll now use a VNC *client* program on your PC/Laptop to connect to the VNC server and take control of it. Follow instructions for your computer's Operating System:

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)

---

*This article uses content from the eLinux wiki page [RPi VNC server](http://elinux.org/RPi_VNC_Server), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
