# Updating and Upgrading Raspbian
There are two steps to upgrading. First run `sudo apt-get update` in order to synchronise the database of available software packages and the versions available. Following this with `sudo apt-get upgrade` will cause any packages which have newer versions available to be updated.

Generally speaking, doing this regularly will keep your installation up to date (i.e. equivalent to the latest released image). However, there are occasionally times where a chance is made in the Foundation's Raspbian image that would require your intervention to reproduce. A recent example would be the addition of the `xserver-xorg-video-fbturbo` X.Org driver to the standard image, which requires people running older images to manually install the package to benefit from it. Cases like this are documented on the relevant image update announcement on the Raspberry Pi blog.

## Running out of space
When running `sudo apt-get upgrade`, an indication of how much data will be downloaded and how much space on the SD card this will take is shown. It's worth checking with `df -h` that you have enough disk space free as unforunately apt will not do this for you. Also be aware that downloaded package files (.deb files) are kept in `/var/cache/apt/archives`. You can remove these in order to free up space with `sudo apt-get clean`.
