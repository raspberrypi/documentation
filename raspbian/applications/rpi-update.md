# rpi-update

`rpi-update` is a command line application that will update your Raspberry Pi OS kernel and VideoCore firmware to the latest pre-release versions.

**WARNING: Pre-release versions of software are not guaranteed to work. You should not use `rpi-update` on any system unless recommended to do so by a Raspberry Pi engineer. It may leave your system unreliable or even completely broken. It should not be used as part of any regular update process.**

The `rpi-update` script is supplied by a third party, "Hexxeh", and also supported by Raspberry Pi engineers. The script source can be found on GitHub at https://github.com/Hexxeh/rpi-update

## What it does

`rpi-update` will download the latest pre-release version of the linux kernel, its matching modules, device tree files, along with the latest versions of the VideoCore firmware. It will then install these files to relevant locations on the SD card, overwriting any previous versions. 

All the source data used by `rpi-update` comes from the GitHub repo https://github.com/Hexxeh/rpi-firmware. This repository simply  contains a subset of the data from the [official firmware repository](https://github.com/raspberrypi/firmware), as not all the data from that repo is required. 

## Running `rpi-update`

If you are sure that you need to use `rpi-update`, it is advisable to take a [backup](../../linux/filesystem/backup.md) of your current system first as running `rpi-update` could result in a non-booting system.

`rpi-update` needs to be run as root. Once the update is complete you will need to reboot.

```
sudo rpi-update
sudo reboot
```

It has a number of options, which are documented at the Hexxeh GitHub repository at https://github.com/Hexxeh/rpi-update

## How to get back to safety

If you have done an `rpi-update` and things are not working as you wish, if your Raspberry Pi is still bootable you can return to the stable release using:

```
sudo apt-get update
sudo apt install --reinstall libraspberrypi0 libraspberrypi-{bin,dev,doc} raspberrypi-bootloader raspberrypi-kernel
```
You will need to reboot your Raspberry Pi for these changes to take effect. 
