# Flashing the Compute Module eMMC

The Compute module has an on-board eMMC device connected to the primary SD card interface. This guide explains how to write data to the eMMC storage using a Compute Module IO Board.

Please also read the section on [Module booting and flashing the eMMC](cm-designguide.md#modulebootingandflashing) in the [Compute Module Hardware Design Guide](cm-designguide.md)

## Steps to flash the eMMC on a Compute Module

You need a host Linux system; a Raspberry Pi will do.  A Mac will not, there is a bug in the BCM2835 bootloader which means we return slightly the wrong information, Windows and Linux don't care and carry on regardless (it's completely benign) but MacOS drops the packet

**On your Compute Module IO Board:**

Make sure that J4 (USB SLAVE BOOT ENABLE) is set to the 'EN' position.

**On your host system:**

Git may produce an error if the date is not set correctly, so on a Raspberry Pi enter the following:

```bash
sudo date MMDDhhmm
```

where MM is month, DD day and hh mm hours and minutes respectively.

Clone the usbboot tool repository and install libusb:

```bash
git clone --depth=1 https://github.com/raspberrypi/tools
cd tools/usbboot
sudo apt-get install libusb-1.0-0-dev
```

Build the usbboot tool:

```bash
make
sudo make install
```

Run the usbboot tool and it will wait for a connection:

```bash
sudo rpiboot
```

Now plug the host machine into the Compute Module IO Board USB slave port (J15) and power on the CMIO board. The usbboot tool will discover the Compute Module and send boot code to allow access to the eMMC. Once complete you will see a new device appear; this is commonly /dev/sda but it could be another location such as /dev/sdb, so check in /dev/ before running rpiboot so you can see what changes.

You now need to write a raw OS image (such as [Raspbian](http://downloads.raspberrypi.org/raspbian_latest)) to the device. Note the following command may take some time to complete, depending on the size of the image:

```bash
sudo dd if=raw_os_image_of_your_choice.img of=/dev/sda bs=4MiB
```

Once the image has been written, unplug and re-plug the USB; you should see 2 partitions appear (for Raspian) in /dev. In total you should see something similar to this:

```bash
/dev/sda    <- Device
/dev/sda1   <- First partition (FAT)
/dev/sda2   <- Second partition (Linux filesystem)
```

The `/dev/sda1` and `/dev/sda2` partitions can now be mounted normally.

Make sure J4 (USB SLAVE BOOT ENABLE) is set to the disabled position and/or nothing is plugged into the USB slave port. Power cycling the IO board should now result in the Compute Module booting from eMMC.
