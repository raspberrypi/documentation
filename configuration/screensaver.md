# Setting the screensaver / screen blanking

## On the console

When running without a graphical desktop, Raspberry Pi OS will blank the screen after 10 minutes without user input, e.g. mouse movement or key presses.

The current setting, in seconds, can be displayed using:
```
cat /sys/module/kernel/parameters/consoleblank
```

To change the `consoleblank` setting, edit the kernel command line:

```
sudo nano /boot/cmdline.txt
```

The file `/boot/cmdline.txt` contains a single line of text. Add `consoleblank=n` to have the console blank after `n` seconds of inactivity. For example `consoleblank=300` will cause the console to blank after 300 seconds, 5 minutes, of inactivity. Make sure that you add your `consoleblank` option to the single line of text already in the `cmdline.txt` file. To disable screen blanking, set `consoleblank=0`.

You can also use the `raspi-config` tool to disable screen blanking. Note that the screen blanking setting in `raspi-config` also controls screen blanking when the graphical desktop is running.

## On the Raspberry Pi desktop

Raspberry Pi OS will blank the graphical desktop after 10 minutes without user input. You can disable this by changing the 'Screen Blanking' option in the Raspberry Pi Configuration tool, which is available on the Preferences menu. Note that the 'Screen Blanking' option also controls screen blanking when the graphical desktop is not running.

There is also a graphical screensaver available, which can be installed as follows:

```
sudo apt install xscreensaver
```

This may take a few minutes.

Once this has been installed, you can find the Screensaver application on the Preferences menu: it provides many options for setting up the screensaver, including disabling it completely.
