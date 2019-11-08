# Setting the screen saver/screen blanking

## On the Console

If you are using the Raspberry Pi solely on the console (no desktop GUI), you need to set the console blanking. The current setting, in seconds, can be displayed using
```
cat /sys/module/kernel/parameters/consoleblank
```

Here, `consoleblank` is a kernel parameter. In order to be permanently set, it needs to be defined on the kernel command line.

```
sudo nano /boot/cmdline.txt
```

Add `consoleblank=0` to turn screen blanking off completely, or edit it to set the number of seconds of inactivity before the console will blank. Note the kernel command line must be a single line of text.

## On the Raspberry Pi Desktop

By default, the Raspberry Pi Desktop does not have any easy-to-use screensaver software installed, although the screensaver is enabled. Firstly, you should install the X Windows screensaver application.

```
sudo apt install xscreensaver
```

This may take a few minutes.

Once this has been installed, you can find the screensaver application under the Preferences option on the main desktop menu. This provides many options for setting up the screensaver, or disabling it completely.
