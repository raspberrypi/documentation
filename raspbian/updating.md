# Updating and Upgrading Raspbian

This section covers how to deploy software updates to devices running Raspbian.

Before we go any further lets investigate why keeping our devices updated is important.

The first and probably the most important reason is security. A device running Raspbian contains millions lines of code which you rely on. Over time these millions lines of code will expose well known vulnerabilities known as [Common Vulnerabilities and Exposures (CVE)](https://cve.mitre.org/index.html), which are documented in publicly available database meaning that they are easy to exploit. Here is a example [link](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-8831) to a recent CVE found in KODI, which provides a bit more insight on what information is available in the database and how they are tracked. The only way to mitigate these exploits as a user of Raspbian is to keep your software up to date as the upstream repositories track CVE's closely and try to mitigate them quickly.

The second reason, which relates to the first is that the software you are running on your device most certainly contains bugs, some bugs are CVE's but could also be something effecting the desired functionality which might not relate to security. By keeping your software up to date, you are lowering the chances of hitting these bugs.

## APT (Advanced Packaging Tool)

To update software in Raspbian, you can use the [apt](../linux/software/apt.md) tool in a terminal window. Open the terminal from the taskbar or application menu:

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

### Updating the kernel and firmware

The kernel and firmware are installed as a Debian package, and so will also get updates when using the procedure above. These packages are updated infrequently and after extensive testing.

### Running out of space

When running `sudo apt-get dist-upgrade`, it will show how much data will be downloaded and how much space it will take up on the SD card. It's worth checking with `df -h` that you have enough free disk space, as unfortunately `apt` will not do this for you. Also be aware that downloaded package files (`.deb` files) are kept in `/var/cache/apt/archives`. You can remove these in order to free up space with `sudo apt-get clean`.

### Upgrading from Jessie to Stretch

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

## Third-party solutions

This section tries to cover why third-party solutions are of interest and why [apt](../linux/software/apt.md) is not optimal for all situations. It also covers existing third-party solutions that support Raspbian.

[Apt](../linux/software/apt.md) is a convenient way of updating the software of your device running Raspbian, but the limitation of this method becomes apparent if you have a larger pool devices to update and especially if you do not have physical access to your device and if they are distributed geographically.

When you lack physical access to your devices and want to deploy unattended updates Over-The-Air(OTA) here are some general requirements:

- It must not under any circumstances break (“brick”) our devices, e.g if the update is interrupted (power-loss, network-loss etc) it should fall-back to a working state
- It must be [atomic](https://en.wikipedia.org/wiki/Atomicity_(database_systems)), update succeeded or update failed. Nothing in-between that could result in that the device still “functions” but with undefined behavior.
- It must be able to install images/packages that are cryptographically signed, preventing third parties from installing software on your device.
- It must be able to install updates using an secure communication channel.

Unfortunately [apt](../linux/software/apt.md) lacks the robustness features, that is atomicity and fall-back. This is why third-party solutions have started to appear trying to solve these problems that are required when deploying unattended updates Over-The-Air.

### Mender

Mender is an end-to-end open source update manager, a robust update process is implemented with atomic dual system update, there is always one working system partition, and Mender updates the one that is not running. You can read more in the [Mender: How it works page](https://mender.io/product/how-it-works).

Mender supports Raspbian. To enable support for Mender in your Raspbian image, follow the tutorial for [Raspbian with Mender](https://hub.mender.io/t/raspberry-pi-3-model-b-b-raspbian/140).
