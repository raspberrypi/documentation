# Setting the screen saver/screen blanking

## On the Console

If you are using the Raspberry Pi solely on the console (No Desktop GUI), you need to set the console blanking. The current setting, in seconds, can be displayed using
```
cat /sys/module/kernel/parameters/consoleblank
```
`consoleblank` is a kernel parameter, that in order to be permanently set, needs to be defined on the kernel command line.
```
sudo nano /boot/cmdline.txt
```
Add `consoleblank=0` to turn screen blanking off completely, or to the number of seconds of inactivity before the console will blank. Note the kernel command line must be a single line of text.

## On the Desktop (Pixel)

By default Pixel does not have any easy to use screensaver software installed, although the screensaver is enabled. So firstly, install the X windows screensaver application.
```
sudo apt-get install xscreensaver
```
This may take a few minutes.

Once installed, you can find the screen saver application under the preferences option on the main desktop menu. This provides many options for setting up the screensaver, or disabling it completely.
