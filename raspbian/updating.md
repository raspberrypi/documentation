# Updating and upgrading Raspberry Pi OS

This section covers how to deploy software updates to devices running Raspberry Pi OS.

Before we go any further, let's investigate why keeping our devices updated is important.

The first and probably the most important reason is security. A device running Raspberry Pi OS contains millions lines of code that you rely on. Over time, these millions lines of code will expose well-known vulnerabilities known as [Common Vulnerabilities and Exposures (CVE)](https://cve.mitre.org/index.html), which are documented in publicly available databases meaning that they are easy to exploit. [Here is a example](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-8831) of a recent CVE found in KODI that provides a bit more insight on what information is available in the database and how CVEs are tracked. The only way to mitigate these exploits as a user of Raspberry Pi OS is to keep your software up to date, as the upstream repositories track CVEs closely and try to mitigate them quickly.

The second reason, which is related to the first, is that the software you are running on your device most certainly contains bugs. Some bugs are CVEs, but bugs could also be affecting the desired functionality without being related to security. By keeping your software up to date, you are lowering the chances of hitting these bugs.

## APT (Advanced Packaging Tool)

To update software in Raspberry Pi OS, you can use the [apt](../linux/software/apt.md) tool in a terminal. Open a terminal window from the taskbar or application menu:

![Terminal](../usage/terminal/images/terminal.png)

First, **update** your system's package list by entering the following command:

```bash
sudo apt update
```

Next, **upgrade** all your installed packages to their latest versions with the following command:

```bash
sudo apt full-upgrade
```

Note that `full-upgrade` is used in preference to a simple `upgrade`, as it also picks up any dependency changes that may have been made. 

Generally speaking, doing this regularly will keep your installation up to date for the particular major Raspberry Pi OS release you are using (e.g. Stretch). It will not update from one major release to another, for example, Stretch to Buster.

However, there are occasional changes made in the Foundation's Raspberry Pi OS image that require manual intervention, for example a newly introduced package. These are not installed with an upgrade, as this command only updates the packages you already have installed.

### Updating the kernel and firmware

The kernel and firmware are installed as a Debian package, and so will also get updates when using the procedure above. These packages are updated infrequently and after extensive testing.

### Running out of space

When running `sudo apt full-upgrade`, it will show how much data will be downloaded and how much space it will take up on the SD card. It's worth checking with `df -h` that you have enough free disk space, as unfortunately `apt` will not do this for you. Also be aware that downloaded package files (`.deb` files) are kept in `/var/cache/apt/archives`. You can remove these in order to free up space with `sudo apt clean` (`sudo apt-get clean` in older releases of apt).

### Upgrading from Stretch to Buster

**Warning**: Upgrading an existing Stretch image is possible, but is not guaranteed to work in every circumstance and we do not recommend it. If you do wish to try upgrading a Stretch image to Buster, we strongly suggest making a backup first — we can accept no responsibility for loss of data from a failed update.

To upgrade, first modify the files `/etc/apt/sources.list` and `/etc/apt/sources.list.d/raspi.list`. In both files, change every occurrence of the word `stretch` to `buster`. (Both files will require sudo to edit.)

Then open a terminal window and execute:

```bash
sudo apt update
sudo apt -y dist-upgrade
```
Answer 'yes' to any prompts. There may also be a point at which the install pauses while a page of information is shown on the screen – hold the <kbd>space</kbd> key to scroll through all of this and then press <kbd>q</kbd> to continue.

Finally, if you are not using PulseAudio for anything other than Bluetooth audio, remove it from the image by entering:

```bash
sudo apt -y purge "pulseaudio*"
```

If moving to a new Pi model (for example the Pi 3B+), you may also need to update the kernel and the firmware using the instructions above.

## Third-party solutions

This section addresses why third-party solutions may be of interest and why [apt](../linux/software/apt.md) is not optimal for all situations. Raspberry Pi do not recommend any specific third-party tools. Prospective users should determine the most suitable tool for their particular requirements.

[Apt](../linux/software/apt.md) is a convenient way of updating the software of your device running Raspberry Pi OS, but the limitation of this method becomes apparent when you have a larger pool of devices to update, and especially when you do not have physical access to your devices and when they are distributed geographically.

If you lack physical access to your devices and want to deploy unattended updates Over-The-Air (OTA), here are some general requirements:

- Updating must not under any circumstances break (“brick”) the devices, e.g if the update is interrupted (power loss, network loss, etc.), the system should fall back to a working state
- Updating must be [atomic](https://en.wikipedia.org/wiki/Atomicity_%28database_systems%29): update succeeded or update failed; nothing in between that could result in a device still “functioning” but with undefined behavior
- Updating must be able to install images/packages that are cryptographically signed, preventing third parties from installing software on your device
- Updating must be able to install updates using an secure communication channel

Unfortunately [apt](../linux/software/apt.md) lacks the robustness features, i.e. atomicity and fall-back. This is why third-party solutions have started to appear that try to solve the problems that need to be addressed for deploying unattended updates OTA.
