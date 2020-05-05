# rpi-update

`rpi-update` is a command line application that will update your Raspbian kernel and Videocore firmware to the latest pre-release versions.

**WARNING: Pre-release versions of software are not guaranteed to work. You should not use `rpi-update` on any system unless recommended to do so by a Raspberry Pi engineer. It may leave your system unreliable or even completely broken. It should not be use as part of any regular update process**

The `rpi-update` script is supplied by a third party, `Hexxeh`, and the source can be found on Github at https://github.com/Hexxeh/rpi-update

## What it does

`rpi-update` will download the latest pre-release version of the linux kernel, it's matching modules, device tree settings, along with the latest version of the Videocore firmware. It will then install these files to the boot partition of the SD card, overwriting any previous versions. 

All the source data used by `rpi-update` comes from the Github repo https://github.com/Hexxeh/rpi-firmware. This repository simply  contains a subset of the data from the official firmware repository, as not all the data from that repo is required. 

## Running `rpi-update`

`rpi-update` needs to be run as root. Once the update is complete you will need to reboot.

```
sudo rpi-update
sudo reboot
```

It has a number of options, which are documented at the Hexxeh Github repository at https://github.com/Hexxeh/rpi-update

## How to get back to safety

If you have done a `rpi-update` and things are not working as you wish, if your Raspberry Pi is still bootable you can return to the stable release using:

```
sudo apt-get update
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
```




