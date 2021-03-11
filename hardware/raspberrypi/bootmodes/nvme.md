# NVMe SSD Boot (BETA)

NVMe (Non Volatile Memory express) is a standard for accessing Solid State Drives (SSD) via a PCI express bus (PCIe). You can connect these drives via the PCIe slot on a Compute Module (CM) IO board allowing a CM4 to boot from SSD.

## Hardware Needed

You need an NVMe M.2 SSD. You can’t plug an M.2 SSD directly into the PCIe slot on the IO board so you’ll need an adapter. Be careful to get the right one. Search for PCI-E 3.0 x1 Lane to M.2 NGFF M-Key SSD Nvme PCI Express Adapter Card.

You don't need it, but if you want to access an NVMe drive from a PC, you might want to get a USB adapter. Search for NVME PCI-E M-Key Solid State Drive External Enclosure.

Linux supports NVMe drives so you should be able to plug it in to the IO board and see your NVMe device to check it works. Run `ls -l /dev/nvme*`.

```
crw------- 1 root root 245, 0 Mar  9 14:58 /dev/nvme0
brw-rw---- 1 root disk 259, 0 Mar  9 14:58 /dev/nvme0n1
```

## Software Needed

To boot from NVMe you need pre-release versions of the bootloader, VideoCore firmware and kernel.

### Bootloader

You need to use [usbboot](https://github.com/raspberrypi/usbboot) to update the CM4 bootloader. See the instructions for how to build rpiboot and configure the IO board to switch the ROM to usbboot mode.

If you are using a CM4 with a eMMC then you will want to change the BOOT_ORDER at this point to give NVMe priority.

```
cd rpiboot/nvme
sed -i 's/\(BOOT_ORDER=.*\)6\(.*\)/\1\26/' boot.conf
./update-pieeprom.sh
cd ..
```

You can then update your bootloader to support NVMe boot with the following command, `./rpiboot -d nvme`

```
Loading: nvme/bootcode4.bin
Waiting for BCM2835/6/7/2711...
Loading: nvme/bootcode4.bin
Sending bootcode.bin
Successful read 4 bytes
Waiting for BCM2835/6/7/2711...
Loading: nvme/bootcode4.bin
Second stage boot server
Loading: nvme/config.txt
File read: config.txt
Loading: nvme/pieeprom.bin
Loading: nvme/pieeprom.bin
Loading: nvme/pieeprom.sig
File read: pieeprom.sig
Loading: nvme/pieeprom.bin
File read: pieeprom.bin
Second stage boot server done
```

### Firmware and Kernel

At the time of writing you need to use pre-release versions of the VideoCore firmware and kernel and these need to be on the NVMe disk. When this software is officially released you will just be able to write the software to the NVMe disk directly with the rpi-imager app. Until then the easiest way to do this is to...

* Boot the board with a blank SSD plugged into the PCIe slot
* Use [piclone](https://github.com/raspberrypi-ui/piclone) to copy the image to the NVMe disk. When using piclone choose the option to use "New Partition ids"
* Update the software on the NVMe disk with the latest pre-release software using [rpi-update](../../../raspbian/applications/rpi-update.md).

```
mkdir mnt
mkdir mnt/fat32
mkdir mnt/ext4
sudo mount /dev/nvme0n1p1 mnt/fat32
sudo mount /dev/nvme0n1p2 mnt/ext4
sudo ROOT_PATH=mnt/ext4 BOOT_PATH=mnt/fat32 rpi-update
```

Finally, if you are using CM4lite remove the SD card and see if the board boots from the NVMe disk. For versions of CM4 with an eMMC you have to make sure the NVMe is first in the boot order.

### NVMe BOOT_ORDER

This boot behavior is controlled via the BOOT_ORDER in the eeprom configuration, we have added a new BOOT_ORDER "6" for NVMe. See [Pi4 Bootloader Configuration](../bcm2711_bootloader_config.md).

This is what you see on the UART if the bootloader detects the drive.

```
Boot mode: SD (01) order f64
Boot mode: USB-MSD (04) order f6
Boot mode: NVME (06) order f
VID 0x144d MN Samsung SSD 970 EVO Plus 250GB
NVME on
```

It should then find a FAT partition and load start4.elf...

```
Read start4.elf bytes  2937840 hnd 0x00050287 hash ''
```

It should then load the kernel and boot the OS.

```
MESS:00:00:07.096119:0: brfs: File read: /mfs/sd/kernel8.img
MESS:00:00:07.098682:0: Loading 'kernel8.img' to 0x80000 size 0x1441a00
MESS:00:00:07.146055:0:[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd083]
```

In linux the SSD appears as /dev/nvme0 and the “namespace” as /dev/nvme0n1. There will be two partitions /dev/nvme0n1p1 (FAT) and /dev/nvme0n1p2 (EXT4). Below we can see that NVMe is used for the boot partition and rootfs "/". Run `lsblk`


```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
nvme0n1     259:0    0 232.9G  0 disk
├─nvme0n1p1 259:1    0   256M  0 part /boot
└─nvme0n1p2 259:2    0 232.6G  0 part /
```

## If something goes wrong

If the boot process fails it would be useful to send us a copy of the console or anything displayed on the screen during boot.

You can enable logging in the bootloader and update the bootloader again with this configuration using usbboot...

```
cd usbboot/nvme
sed -i 's/BOOT_UART=0/BOOT_UART=1/' boot.conf
./update-pieeprom.sh
cd ..
./rpiboot -d nvme
```

Enable UART logging in `/boot/config.txt` to allow you to capture logs from the serial port.

```
# UART console
enable_uart=1

# UART from firmware
uart_2ndstage=1
```

Check you have the right version of the start4.elf VideoCore firmware by checking the version of the raspberrypi-bootloader package, it should show a date on or after 3 Mar 2021 in the version string. Run `apt show raspberrypi-bootloader`

```
Package: raspberrypi-bootloader
Version: 1.20210303-1
```

If you see an error on boot “start4.elf: is not compatible” on the UART console, then you are using an old version of this binary.

You need an updated version of the kernel that includes support for NVMe (previously it was built as a module). Without this the kernel will wait forever for the disk to appear. So check the kernel version by running `uname -a`

```
Linux raspberrypi 5.10.20-v7l+ #1404 SMP Thu Mar 4 19:44:07 GMT 2021 armv7l GNU/Linux
```

If there’s a compatibility issue with the SSD then you can use the following commands to interrogate the device...

```
sudo apt-get install nvme-cli
sudo nvme list
sudo nvme id-ctrl -H /dev/nvme0
sudo nvme list-ns /dev/nvme0
sudo nvme id-ns -H /dev/nvme0 --namespace-id=1
```

It would be helpful to post the output of these commands in any error report.
