# How to boot from a USB Mass Storage Device on a Raspberry Pi 3
This tutorial explains how to boot your Raspberry Pi 3 from a USB mass storage device such as a flash drive or USB hard disk. Be warned that this feature is experimental and may not work with all USB mass storage devices.

## Program USB Boot Mode
Before a Raspberry Pi will boot from a mass storage device, it needs to be booted from an SD card with a config option to enable USB boot mode. This will set a bit in the OTP (One Time Programmable) memory in the Raspberry Pi SoC that enables network booting. Once this is done, the SD card is no longer required. 

Install Raspbian Lite (or Raspbian with PIXEL) on the SD card in the normal way [See here](../../../installation/installing-images/README.md).

First, prepare the `/boot` directory with up to date boot files:
```
$ sudo apt-get update
```
Then enable USB boot mode with this code:
```
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```

This adds `program_usb_boot_mode=1` to the end of `/boot/config.txt`. Reboot the Raspberry Pi with `sudo reboot`, then check that the OTP has been programmed with:

```
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Ensure the output `0x3020000a` is correct.

If you wish, you can remove the `program_usb_boot_mode` line from config.txt, so that if you put the SD card in another Raspberry Pi, it won't program USB boot mode. Make sure there is no blank line at the end of config.txt. You can do this with `sudo nano /boot/config.txt`, for example.

## Prepare the USB storage device
Now that your Raspberry Pi is USB boot-enabled, you can prepare a USB storage device to boot from. Start by inserting the USB storage device into the Raspberry Pi. Note that the USB storage device will be completely erased. Rather than downloading the Raspbian image again, we will copy it from the SD card on the Raspberry Pi. The source device (SD card) will be `/dev/mmcblk0` and the destination device (USB disk) should be `/dev/sda`, assuming you have no other USB devices connected.

We will start by using Parted to create a 100MB FAT32 partition, followed by a Linux ext4 partition that will take up the rest of the disk.

```
sudo parted /dev/sda

(parted) mktable msdos
Warning: The existing disk label on /dev/sda will be destroyed and all data on this disk will be lost. Do you want to continue?
Yes/No? Yes
(parted) mkpart primary fat32 0% 100M
(parted) mkpart primary ext4 100M 100%
(parted) print
Model: SanDisk Ultra (scsi)
Disk /dev/sda: 30.8GB
Sector size (logical/physical): 512B/512B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  99.6MB  98.6MB  primary  fat32        lba
 2      99.6MB  30.8GB  30.7GB  primary  ext4         lba
```
Your `parted print` output should look similar to the one above.

Type `quit` to exit parted.

Create the boot and root file systems:
```
sudo mkfs.vfat -n BOOT -F 32 /dev/sda1
sudo mkfs.ext4 /dev/sda2
```

Mount the target file system and copy the running Raspbian system to it:
```
sudo mkdir /mnt/target
sudo mount /dev/sda2 /mnt/target/
sudo mkdir /mnt/target/boot
sudo mount /dev/sda1 /mnt/target/boot/
sudo apt-get update; sudo apt-get install rsync
sudo rsync -ax --progress / /boot /mnt/target
```

Regenerate SSH host keys:
```
cd /mnt/target
sudo mount --bind /dev dev
sudo mount --bind /sys sys
sudo mount --bind /proc proc
sudo chroot /mnt/target
rm /etc/ssh/ssh_host*
dpkg-reconfigure openssh-server
exit
sudo umount dev
sudo umount sys
sudo umount proc
```

Edit `/boot/cmdline.txt` so that it uses the USB storage device as the root file system, instead of the SD card.

```
sudo sed -i "s,root=/dev/mmcblk0p2,root=/dev/sda2," /mnt/target/boot/cmdline.txt
```

The same needs to be done for `fstab`:
```
sudo sed -i "s,/dev/mmcblk0p,/dev/sda," /mnt/target/etc/fstab
```

Finally, unmount the target file systems, and power the Raspberry Pi off.
```
cd ~
sudo umount /mnt/target/boot 
sudo umount /mnt/target
sudo poweroff 
```

Disconnect the power supply from the Raspberry Pi, remove the SD card, and reconnect the power supply. If all has gone well, the Raspberry Pi should begin to boot after a few seconds.
