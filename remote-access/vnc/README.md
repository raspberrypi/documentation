# VNC (Virtual Network Computing)

Sometimes it is not convenient to work directly on the Raspberry Pi. Maybe you would like to work on it from another computer by remote control.

VNC is a graphical desktop sharing system that allows you to remotely control the desktop interface of one computer from another. It transmits the keyboard and mouse events from the controller, and receives updates to the screen over the network from the remote host.

You will see the desktop of the Raspberry Pi inside a window on your computer. You'll be able to control it as though you were working on the Raspberry Pi itself.

- On your Pi (using a monitor or via [SSH](../ssh/README.md)), install the TightVNC package:

```
sudo apt-get install tightvncserver
```

- Next, run TightVNC Server which will prompt you to enter a password and an optional view-only password:

```
tightvncserver
```

- Start a VNC server from the terminal. This example starts a session on VNC display zero (```:0```) with full HD resolution:

```
vncserver :0 -geometry 1920x1080 -depth 24
```

- Now, on your computer, install and run the VNC client:

  - On a Linux machine install the package `xtightvncviewer`:

    `sudo apt-get install xtightvncviewer`

  - Otherwise, TightVNC is downloadable from [tightvnc.com](http://www.tightvnc.com/download.php)

### Automation and run at boot

You can create a simple file with the command to run the VNC server on the Pi, to save having to remember it:

- Create a file containing the following shell script:

```
#!/bin/sh
vncserver :0 -geometry 1920x1080 -depth 24 -dpi 96
```

- Save this as ```vnc.sh``` (for example)

- Make the file executable:

```
chmod +x vnc.sh
```

- Then you can run it at any time with:

```
./vnc.sh
```

To run at boot:

- Log into a terminal on the Pi as root:

```
sudo su
```

- Navigate to the directory ```/etc/init.d/```:

```
cd /etc/init.d/
```

- Create a new file here containing the following script:

```
#! /bin/sh
# /etc/init.d/vncboot

### BEGIN INIT INFO
# Provides: vncboot
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start VNC Server at boot time
# Description: Start VNC Server at boot time.
### END INIT INFO

USER=pi
HOME=/home/pi

export USER HOME

case "$1" in
 start)
  echo "Starting VNC Server"
  #Insert your favoured settings for a VNC session
  su - pi -c "/usr/bin/vncserver :0 -geometry 1280x800 -depth 16 -pixelformat rgb565"
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

- Save this file as ```vncboot``` (for example)

- Make this file executable:

```
chmod 755 vncboot
```

- Enable dependency-based boot sequencing:

```
update-rc.d /etc/init.d/vncboot defaults
```

- If enabling dependency-based boot sequencing was successful, you will see this:

```
update-rc.d: using dependency based boot sequencing
```

- But if you see this:

```
update-rc.d: error: unable to read /etc/init.d//etc/init.d/vncboot
```

- then try the following command:

```
update-rc.d vncboot defaults
```

- Reboot your Raspberry Pi and you should find a VNC server already started.

You'll now use a VNC **client** program on your PC/laptop to connect to the VNC server and take control of it. Follow instructions for your computer's operating system:

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)

---

*This article uses content from the eLinux wiki page [RPi VNC server](http://elinux.org/RPi_VNC_Server), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
