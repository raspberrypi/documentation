# Updating and Upgrading Raspbian

There are two steps to upgrading. First, run `sudo apt-get update` in order to synchronise the database of available software packages and the versions available. Next, run `sudo apt-get upgrade` which will cause any packages with newer versions available to be updated.

Generally speaking, doing this regularly will keep your installation up to date; in other words, it will be equivalent to the latest released image. However, there are occasionally times where a change is made in the Foundation's Raspbian image that require your intervention to reproduce. A recent example is the addition of the `xserver-xorg-video-fbturbo` X.Org driver to the standard image; this requires users running older images to manually install the package to benefit from it. Cases like this are documented on the relevant image update announcement on the Raspberry Pi blog.

## Updating the kernel and firmware

The kernel and firmware are installed as a Debian package, and so will also get updates when using the procedure above. These packages are updated infrequently (after extensive testing); if you want to try more recent experimental software, it's also easy to update to the latest available version using [rpi-update](https://github.com/Hexxeh/rpi-update). This is pre-installed on the current Raspbian image, so you can just use `sudo rpi-update` to try the latest firmware; this will sometimes be suggested when troubleshooting. If you receive errors about invalid certificates, then run `sudo apt-get update && sudo apt-get install rpi-update` to upgrade to the latest rpi-update version.

## Running out of space

When running `sudo apt-get upgrade`, it will show how much data will be downloaded and how much space it will take up on the SD card. It's worth checking with `df -h` that you have enough disk space free, as unfortunately apt will not do this for you. Also be aware that downloaded package files (.deb files) are kept in `/var/cache/apt/archives`. You can remove these in order to free up space with `sudo apt-get clean`.
