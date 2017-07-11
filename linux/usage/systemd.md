# systemd

In order to have a command or program run when the Pi boots, you can add it as a service.
Once this is done you can start/stop enable/disable from the linux prompt

## Creating a service

On your Pi, create a .service file for your service e.g.

myscript.service

```[Unit]
Description=My service
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u main.py
WorkingDirectory=/home/pi/myscript
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
So in this instance the service would run python3 from our working directory /home/pi/myscript which contains our python program to run myscript.py. But you are not limited to python programs, simply change the ExecStart line to be the command to start any program/script that you want running from startup.

Copy this file into /lib/systemd/system as root e.g.
```
sudo cp myscript.service /lib/systemd/system/myscript.service
```

Once this has been copied you can attempt to start the service using
```
sudo systemctl start myscript.service
```

and stop it using
```
sudo systemctl stop myscript.service
```
When you are happy that this starts and stops your app, then you can have it start automatically on reboot by using
```
sudo systemctl enable myscript.service
```

The systemctl command can also be used to restart the service or disable it from boot up as well!

Some things to be aware of:
The order of when things are started is based on their dependancies, this particular script should start fairly late in the boot process, after a network is available (see the After section).
You can configure different dependancies and orders based on your requirements.


You can get more information from
``` man systemctl```
or from https://fedoramagazine.org/what-is-an-init-system/

Also, be sure to reference absolute filenames rather than relative to your home folder; for example, `/home/pi/myscript.py` rather than `myscript.py`.
