# Updating and Upgrading Raspbian

First, **update** your system's package list by entering the following command in LXTerminal or from the command line:

```bash
sudo apt-get update
```

Next, **upgrade** all your installed packages to their latest versions with the command:

```bash
sudo apt-get upgrade
```

Generally speaking, doing this regularly will keep your installation up to date, in that it will be equivalent to the latest released image available from [raspberrypi.org/downloads](http://www.raspberrypi.org/downloads/).

However, there are occasional changes made in the Foundation's Raspbian image that require manual intervention, for example a newly introduced package. These are not installed with an upgrade, as this command only updates the packages you already have installed.

## Updating the kernel and firmware

The kernel and firmware are installed as a Debian package, and so will also get updates when using the procedure above. These packages are updated infrequently (after extensive testing); if you want to try more recent experimental software, it's also easy to update to the latest available version using the [rpi-update](https://github.com/Hexxeh/rpi-update) tool.

To run this update, simply run from the command line:

```bash
sudo rpi-update
```

You'll need the latest version of the tool, so make sure you've recently run `apt-get update` and `upgrade` first.

Your system date/time will need to be accurate too, or it will fail to communicate with the server. To manually set your system time, run the following command (with the *actual* time and date):

```bash
sudo date -s "8 JAN 2015 12:00:00"
```

## Running out of space

When running `sudo apt-get upgrade`, it will show how much data will be downloaded and how much space it will take up on the SD card. It's worth checking with `df -h` that you have enough disk space free, as unfortunately `apt` will not do this for you. Also be aware that downloaded package files (`.deb` files) are kept in `/var/cache/apt/archives`. You can remove these in order to free up space with `sudo apt-get clean`.
