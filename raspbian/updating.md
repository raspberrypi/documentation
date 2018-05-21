# Updating and Upgrading Raspbian

To update software in Raspbian, you'll need to use the [apt](../linux/software/apt.md) tool in a terminal window. Open the terminal from the taskbar or application menu:

![Terminal](../usage/terminal/images/terminal.png)

First, **update** your system's package list by entering the following command:

```bash
sudo apt-get update
```

Next, **upgrade** all your installed packages to their latest versions with the command:

```bash
sudo apt-get dist-upgrade
```

Generally speaking, doing this regularly will keep your installation up to date, in that it will be equivalent to the latest released image available from [raspberrypi.org/downloads](https://www.raspberrypi.org/downloads/).

However, there are occasional changes made in the Foundation's Raspbian image that require manual intervention, for example a newly introduced package. These are not installed with an upgrade, as this command only updates the packages you already have installed.

## Updating the kernel and firmware

The kernel and firmware are installed as a Debian package, and so will also get updates when using the procedure above. These packages are updated infrequently and after extensive testing.

## Running out of space

When running `sudo apt-get dist-upgrade`, it will show how much data will be downloaded and how much space it will take up on the SD card. It's worth checking with `df -h` that you have enough free disk space, as unfortunately `apt` will not do this for you. Also be aware that downloaded package files (`.deb` files) are kept in `/var/cache/apt/archives`. You can remove these in order to free up space with `sudo apt-get clean`.

## Upgrading from Jessie to Stretch

Upgrading an existing Jessie image is possible, but is not guaranteed to work in every circumstance. If you wish to try upgrading a Jessie image to Stretch, we strongly recommend making a backup first — we can accept no responsibility for loss of data from a failed update.

To upgrade, first modify the files `/etc/apt/sources.list` and `/etc/apt/sources.list.d/raspi.list`. In both files, change every occurrence of the word `jessie` to `stretch`. (Both files will require sudo to edit.)

Then open a terminal window and execute:

```bash
sudo apt-get update
sudo apt-get -y dist-upgrade
```
Answer 'yes' to any prompts. There may also be a point at which the install pauses while a page of information is shown on the screen – hold the <kbd>space</kbd> key to scroll through all of this and then press <kbd>q</kbd> to continue.

Finally, if you are not using PulseAudio for anything other than Bluetooth audio, remove it from the image by entering:

```
sudo apt-get -y purge "pulseaudio*"
```

If moving to a new Pi model (for example the Pi 3B+), you may also need to update the kernel and the firmware using the instructions above.
