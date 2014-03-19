# Kernel Building

There are two main methods for building the kernel: locally on a Raspberry Pi (be prepared to wait!); or cross-compiled (much quicker, but requires more setup)

## Local building

On a Raspberry Pi first install the latest version of [Raspbian](http://www.raspberrypi.org/downloads) from the downloads page. Then boot your Pi, plug in ethernet (to give you access to the sources) and log in.

First get the sources: (takes a bit of time...)

```
$ git clone --depth=1 https://github.com/raspberrypi/linux
```

Add missing dependencies:

```
$ sudo apt-get install bc
```

Build the kernel (takes a _lot_ of time...)

```
$ make bcmrpi_defconfig
$ make
$ make modules
$ sudo make modules_install
$ sudo cp arch/arm/boot/Image /boot/kernel.img
```

## Cross compiling

First you are going to require a suitable Linux cross compilation host, we tend to use Ubuntu since Raspbian is 
also a debian distribution it means using similar command lines etc!

You can either do this using VirtualBox (or VMWare) on Windows or install it directly onto your computer.  For reference I'd suggest following instructions online http://www.wikihow.com/Install-Ubuntu-on-VirtualBox

### Install toolchain

```
$ git clone https://github.com/raspberrypi/tools
```

You can then copy the toolchain somewhere common, I tend to install mine to /tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian and add a path to that directory into the .bashrc in your home directory although that is not strictly necessary it does make it easier for later command lines!

### Get sources

To get the sources, refer to the original github repository for the various branches.  https://github.com/raspberrypi/linux

```
$ git clone --depth=1 https://github.com/raspberrypi/linux
```

### Build sources

To build the sources for cross compilation there may be extra dependancies over and above what you've installed by default with Ubuntu (I'm assuming above git was already installed for example!).  If you find you need other things please submit a pull request to change the documentation!  Thanks

```
$ cd linux
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi-defconfig
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-
```

Note to speed up compilation on multiprocessor systems (and get some improvement on single processor ones) use ```-j n``` where n is number of processors * 1.5 or play around and see what works!

### Install

Now having built the kernel you need to copy the it onto your Raspberry Pi and install the modules, this is best done directly using an SD card reader.

First use lsblk before and after plugging in your sdcard to identify which one it is, you should end up with something like:

```
sdb
   sdb1
   sdb2
```

Unless it is a NOOBS card in which case you should see something like:

```
sdb
  sdb1
  sdb2
  sdb3
  sdb5
  sdb6
```

It the first case [sdb1/sdb5] is the FAT partition [sdb2/sdb6] is the ext4 filesystem [image / NOOBS]

So mount these first

```
$ mkdir mnt/fat32
$ mkdir mnt/ext4
$ sudo mount /dev/sdb1 mnt/fat32
$ sudo mount /dev/sdb2 mnt/ext4
```

Adjust partition numbers for NOOBS images

Next install the modules

```
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules
$ sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install
```

Finally copy the kernel onto the SD card

```
$ sudo cp arch/arm/boot/Image mnt/fat32/kernel.img
$ sudo umount mnt/fat32
$ sudo umount mnt/ext4
```

Unplug the card and boot the Pi!

## Links

Building / cross compiling on/for other operating systems
- Pidora
- ArchLinux
- RaspBMC
- OpenELEC
