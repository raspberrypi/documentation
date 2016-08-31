# VNC (Virtual Network Computing)

Sometimes it is not convenient to work directly on the Raspberry Pi. Maybe you would like to work on it from another computer by remote control.

VNC is a graphical desktop sharing system that allows you to remotely control the desktop interface of one computer from another. It transmits the keyboard and mouse events from the controller, and receives updates to the screen over the network from the remote host.

You will see the desktop of the Raspberry Pi inside a window on your computer. You'll be able to control it as though you were working on the Raspberry Pi itself.

- On your Pi (using a monitor or via [SSH](../ssh/README.md)), install the TightVNC package:

    ```bash
    sudo apt-get install tightvncserver
    ```

- Next, run TightVNC Server which will prompt you to enter a password and an optional view-only password:

    ```bash
    tightvncserver
    ```

- Start a VNC server from the terminal:  This example starts a session on VNC display one (```:1```) with full HD resolution:

    ```bash
    vncserver :1 -geometry 1920x1080 -depth 24
    ```

    Note that since by default an X session is started on display zero, you will get an error in case you use `:0`.

- Since there are now two X sessions running, which would normally be a waste of resources, it is suggested to stop the displaymanager running on ```:0``` using

    ```bash
    service lightdm stop
    ```
    
- Now, on your computer, install and run the VNC client:

    - On a Linux machine install the package `xtightvncviewer`:

    ```bash
    sudo apt-get install xtightvncviewer
    ```

    - Otherwise, TightVNC is downloadable from [tightvnc.com](http://www.tightvnc.com/download.php)

### Automation and run at boot

You can create a simple file with the command to run the VNC server on the Pi, to save having to remember it:

- Create a file containing the following shell script:

    ```bash
    #!/bin/sh
    vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96
    ```

- Save this as `vnc.sh` (for example)

- Make the file executable:

    ```bash
    chmod +x vnc.sh
    ```

- Then you can run it at any time with:

    ```bash
    ./vnc.sh
    ```

- If you prefer your mouse pointer in the VNC client to appear as an arrow as opposed to an "x" which is default, in `/home/pi/.vnc/xstartup` add the following parameter to `xsetroot`:

    ```bash
    -cursor_name left_ptr
    ```

To run at boot:

- Log into a terminal on the Pi as root:

    ```bash
    sudo su
    ```

- Navigate to the directory `/etc/init.d/`:

    ```bash
    cd /etc/init.d/
    ```

- Create a new file here containing the following script:

    ```bash
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
      su - $USER -c "/usr/bin/vncserver :1 -geometry 1280x800 -depth 16 -pixelformat rgb565"
      ;;
    
     stop)
      echo "Stopping VNC Server"
      /usr/bin/vncserver -kill :1
      ;;
    
     *)
      echo "Usage: /etc/init.d/vncboot {start|stop}"
      exit 1
      ;;
    esac
    
    exit 0
    ```

- Save this file as `vncboot` (for example)

- Make this file executable:

    ```bash
    chmod 755 vncboot
    ```

- Enable dependency-based boot sequencing:

    ```bash
    update-rc.d -f lightdm remove
    update-rc.d vncboot defaults
    ```

- If enabling dependency-based boot sequencing was successful, you will see this:

    ```bash
    update-rc.d: using dependency based boot sequencing
    ```

- Reboot your Raspberry Pi and you should find a VNC server already started.

You'll now use a VNC **client** program on your PC/laptop to connect to the VNC server and take control of it. Follow instructions for your computer's operating system:

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)

---

*This article uses content from the eLinux wiki page [RPi VNC server](http://elinux.org/RPi_VNC_Server), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
