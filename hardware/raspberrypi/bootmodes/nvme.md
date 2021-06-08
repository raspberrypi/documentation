# NVMe SSD Boot (BETA)

NVMe (non-volatile memory express) is a standard for accessing solid state drives (SSDs) via a PCIe bus. You can connect these drives via the PCIe slot on a Compute Module 4 (CM4) IO board, allowing a CM4 to boot from SSD.

## Required hardware

You need an NVMe M.2 SSD. You cannot plug an M.2 SSD directly into the PCIe slot on the IO board - an adaptor is needed. Be careful to get the correct type: a suitable adaptor can be found online by searching for 'PCI-E 3.0 x1 Lane to M.2 NGFF M-Key SSD Nvme PCI Express Adapter Card'.

Raspberry Pi OS supports accessing NVMe drives, although booting from NVMe is currently only supported using pre-release software (see 'required software' below). To check that your NVMe drive is connected correctly, boot Raspberry Pi OS from another drive and run `ls -l /dev/nvme*`; example output is shown below.

```
crw------- 1 root root 245, 0 Mar  9 14:58 /dev/nvme0
brw-rw---- 1 root disk 259, 0 Mar  9 14:58 /dev/nvme0n1
```

If you need to connect the NVMe drive to a PC or Mac you can use a USB adaptor: search for 'NVME PCI-E M-Key Solid State Drive External Enclosure'. The enclosure must support M key SSDs.

## Required software

To boot from NVMe you need pre-release versions of the bootloader, VideoCore firmware and Raspberry Pi OS Linux kernel.

### Bootloader

You need to use `rpiboot` to update the CM4 bootloader. Instructions for building `rpiboot` and configuring the IO board to switch the ROM to usbboot mode are in the [usbboot Github repository](https://github.com/raspberrypi/usbboot).

If you are using a CM4 with an eMMC then you must change the BOOT_ORDER to give NVMe priority, otherwise the CM4 will continue to boot from eMMC. For example:

```
cd usbboot/nvme
sed -i 's/\(BOOT_ORDER=.*\)6\(.*\)/\1\26/' boot.conf
./update-pieeprom.sh
cd ..
```

You can then update your bootloader to support NVMe boot with `./rpiboot -d nvme`; example output is shown below.

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

### Firmware and kernel

You must load pre-release versions of the VideoCore firmware and Raspberry Pi OS Linux kernel to the NVMe disk. When this software is officially released you can simply write the software to the NVMe disk directly with the Raspberry Pi Imager app; until then the easiest way to perform the update is:

1. Boot the CM4 with a blank SSD connected to the PCIe slot
1. Use the `SD Card Copier` application on the desktop to copy the running OS image to the NVMe disk, making sure to enable the "new partition ids" option.
1. Update the firmware and kernel on the NVMe disk to the latest pre-release versions using [rpi-update](../../../raspbian/applications/rpi-update.md):
```
mkdir mnt
mkdir mnt/fat32
mkdir mnt/ext4
sudo mount /dev/nvme0n1p1 mnt/fat32
sudo mount /dev/nvme0n1p2 mnt/ext4
sudo ROOT_PATH=mnt/ext4 BOOT_PATH=mnt/fat32 rpi-update
```

Finally, if you are using CM4 lite, remove the SD card and the board will boot from the NVMe disk. For versions of CM4 with an eMMC, make sure you have set NVMe first in the boot order.

### NVMe BOOT_ORDER

This boot behaviour is controlled via the `BOOT_ORDER` setting in the EEPROM configuration: we have added a new boot mode `6` for NVMe. See [Raspberry Pi 4 Bootloader Configuration](../bcm2711_bootloader_config.md).

Below is an example of UART output when the bootloader detects the NVMe drive:

```
Boot mode: SD (01) order f64
Boot mode: USB-MSD (04) order f6
Boot mode: NVME (06) order f
VID 0x144d MN Samsung SSD 970 EVO Plus 250GB
NVME on
```

It will then find a FAT partition and load `start4.elf`:

```
Read start4.elf bytes  2937840 hnd 0x00050287 hash ''
```

It will then load the kernel and boot the OS:

```
MESS:00:00:07.096119:0: brfs: File read: /mfs/sd/kernel8.img
MESS:00:00:07.098682:0: Loading 'kernel8.img' to 0x80000 size 0x1441a00
MESS:00:00:07.146055:0:[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd083]
```

In Linux the SSD appears as `/dev/nvme0` and the "namespace" as `/dev/nvme0n1`. There will be two partitions `/dev/nvme0n1p1` (FAT) and `/dev/nvme0n1p2` (EXT4). Use `lsblk` to check the partition assignments:


```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
nvme0n1     259:0    0 232.9G  0 disk
├─nvme0n1p1 259:1    0   256M  0 part /boot
└─nvme0n1p2 259:2    0 232.6G  0 part /
```

## Troubleshooting

If the boot process fails, please file an issue on the [rpi-eeprom Github repository](https://github.com/raspberrypi/rpi-eeprom), including a copy of the console and anything displayed on the screen during boot.

You can enable logging in the bootloader, and update the bootloader with this configuration, using `rpiboot`:

```
cd usbboot/nvme
sed -i 's/BOOT_UART=0/BOOT_UART=1/' boot.conf
./update-pieeprom.sh
cd ..
./rpiboot -d nvme
```

Enable UART logging in `/boot/config.txt` to allow you to capture logs from the serial port:

```
# UART console
enable_uart=1

# UART from firmware
uart_2ndstage=1
```

Ensure that you have used `rpi-update` to get the latest pre-release versions of the firmware and Linux kernel; boot from NVMe will not work without these.

There may be compatibility issues with some SSDs. You can use the following commands to investigate:

```
sudo apt-get install nvme-cli
sudo nvme list
sudo nvme id-ctrl -H /dev/nvme0
sudo nvme list-ns /dev/nvme0
sudo nvme id-ns -H /dev/nvme0 --namespace-id=1
```

Please post the output of these commands in any error report.
