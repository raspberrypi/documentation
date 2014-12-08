# Kernel Building

There are two main methods for building the kernel. You can build locally on a Raspberry Pi which will take a long time; or you can cross-compile, which is much quicker, but requires more setup.

## Local building

On a Raspberry Pi first install the latest version of [Raspbian](http://www.raspberrypi.org/downloads) from the downloads page. Then boot your Pi, plug in Ethernet to give you access to the sources, and log in.

First get the sources, which will take some time:

```
$ git clone --depth=1 https://github.com/raspberrypi/linux
```

Add missing dependencies:

```
$ sudo apt-get install bc
```

Configure the kernel - as well as the default configuration you may wish to [configure your kernel in more detail](configuring.md) or [apply patches from another source](patching.md) to add or remove required functionality:

```
$ cd linux
$ make bcmrpi_defconfig
```

Build the kernel; this step takes a **lot** of time...

```
$ make
$ make modules
$ sudo make modules_install
$ sudo cp arch/arm/boot/Image /boot/kernel.img
```

## Cross-compiling

First you are going to require a suitable Linux cross-compilation host. We tend to use Ubuntu; since Raspbian is 
also a Debian distribution it means using similar command lines and so on.

You can either do this using VirtualBox (or VMWare) on Windows, or install it directly onto your computer. For reference you can follow instructions online [at Wikihow](http://www.wikihow.com/Install-Ubuntu-on-VirtualBox).

### Install toolchain

Use the following command:

```
$ git clone https://github.com/raspberrypi/tools
```

You can then copy the toolchain to a common location such as `/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian`, and add `/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin` to your $PATH in the .bashrc in your home directory. While this step is not strictly necessary, it does make it easier for later command lines!

### Get sources

To get the sources, refer to the original [GitHub](https://github.com/raspberrypi/linux) repository for the various branches.
```
$ git clone --depth=1 https://github.com/raspberrypi/linux
```

### Build sources

To build the sources for cross-compilation there may be extra dependencies beyond those you've installed by default with Ubuntu. If you find you need other things please submit a pull request to change the documentation.

Enter the following commands to build the sources:

```
$ cd linux
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-
```

Note: To speed up compilation on multiprocessor systems, and get some improvement on single processor ones, use ```-j n``` where n is number of processors * 1.5. Alternatively, feel free to experiment and see what works!

### Install

Having built the kernel you need to copy it onto your Raspberry Pi and install the modules; this is best done directly using an SD card reader.

First use lsblk before and after plugging in your SD card to identify which one it is; you should end up with something like this:

```
sdb
   sdb1
   sdb2
```

If it is a NOOBS card you should see something like this:

```
sdb
  sdb1
  sdb2
  sdb3
  sdb5
  sdb6
```

In the first case `sdb1/sdb5` is the FAT partition, and `sdb2/sdb6` is the ext4 filesystem image (NOOBS).

Mount these first:

```
$ mkdir mnt/fat32
$ mkdir mnt/ext4
$ sudo mount /dev/sdb1 mnt/fat32
$ sudo mount /dev/sdb2 mnt/ext4
```

Adjust the partition numbers for the NOOBS images.

Next, install the modules:

```
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules
$ sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install
```

Finally, copy the kernel onto the SD card, making sure to back up your old kernel:

```
$ sudo cp mnt/fat32/kernel.img mnt/fat32/kernel-backup.img
$ sudo cp arch/arm/boot/Image mnt/fat32/kernel.img
$ sudo umount mnt/fat32
$ sudo umount mnt/ext4
```

Another option is to copy the kernel into the same place, but with a different filename - for instance, kernel-myconfig.img - rather than overwriting the kernel.img file. You can then edit the config.txt file to select the kernel that the Pi will boot into.

```
kernel=kernel-myconfig.img
```

This has the advantage of keeping your kernel separate from the kernel image managed by the system and any automatic update tools, and allowing you to easily revert to a stock kernel in the event that your kernel cannot boot.

Unplug the card and boot the Pi!

## Links

Building / cross-compiling on/for other operating systems

- Pidora
- ArchLinux
- RaspBMC
- OpenELEC
