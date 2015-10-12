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

Run the following commands depending on your Raspberry Pi version.

####Raspberry Pi 1 (or Compute Module) Default Build Configuration

```
$ cd linux
$ KERNEL=kernel
$ make bcmrpi_defconfig
```

####Raspberry Pi 2 Default Build Configuration
```
$ cd linux
$ KERNEL=kernel7
$ make bcm2709_defconfig
```
Build and install the kernel, modules and Device Tree blobs; this step takes a **lot** of time...

```
$ make zImage modules dtbs
$ sudo make modules_install
$ sudo cp arch/arm/boot/dts/*.dtb /boot/
$ sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
$ sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
$ sudo scripts/mkknlimg arch/arm/boot/zImage /boot/$KERNEL.img
```
Note: On a Raspberry Pi 2, adding `-j4` (`make -j4 zImage modules dtbs`) splits the work between all four cores, speeding up compilation significantly.

## Cross-compiling

First you are going to require a suitable Linux cross-compilation host. We tend to use Ubuntu; since Raspbian is 
also a Debian distribution it means using similar command lines and so on.

You can either do this using VirtualBox (or VMWare) on Windows, or install it directly onto your computer. For reference you can follow instructions online [at Wikihow](http://www.wikihow.com/Install-Ubuntu-on-VirtualBox).

### Install toolchain

Use the following command:

```
$ git clone https://github.com/raspberrypi/tools
```

You can then copy the toolchain to a common location such as `/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian`, and add `/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin` to your $PATH in the .bashrc in your home directory.
For 64bit, use /tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin.
While this step is not strictly necessary, it does make it easier for later command lines!

### Get sources

To get the sources, refer to the original [GitHub](https://github.com/raspberrypi/linux) repository for the various branches.
```
$ git clone --depth=1 https://github.com/raspberrypi/linux
```

### Build sources

To build the sources for cross-compilation there may be extra dependencies beyond those you've installed by default with Ubuntu. If you find you need other things please submit a pull request to change the documentation.

Enter the following commands to build the sources and Device Tree files.

For Pi 1 or Compute Module:
```
$ cd linux
$ KERNEL=kernel
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig
```
For Pi 2:
```
$ cd linux
$ KERNEL=kernel7
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig
```
Then for both:
```
$ make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs
```

Note: To speed up compilation on multiprocessor systems, and get some improvement on single processor ones, use ```-j n``` where n is number of processors * 1.5. Alternatively, feel free to experiment and see what works!

### Install directly onto the SD card

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
$ sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install
```

Finally, copy the kernel and Device Tree blobs onto the SD card, making sure to back up your old kernel:

```
$ sudo cp mnt/fat32/$KERNEL.img mnt/fat32/$KERNEL-backup.img
$ sudo scripts/mkknlimg arch/arm/boot/zImage mnt/fat32/$KERNEL.img
$ sudo cp arch/arm/boot/dts/*.dtb mnt/fat32/
$ sudo cp arch/arm/boot/dts/overlays/*.dtb* mnt/fat32/overlays/
$ sudo cp arch/arm/boot/dts/overlays/README mnt/fat32/overlays/
$ sudo umount mnt/fat32
$ sudo umount mnt/ext4
```

Another option is to copy the kernel into the same place, but with a different filename - for instance, kernel-myconfig.img - rather than overwriting the kernel.img file. You can then edit the config.txt file to select the kernel that the Pi will boot into:

```
kernel=kernel-myconfig.img
```

This has the advantage of keeping your kernel separate from the kernel image managed by the system and any automatic update tools, and allowing you to easily revert to a stock kernel in the event that your kernel cannot boot.

Finally, plug the card into the Pi and boot it!

## Links

Building / cross-compiling on/for other operating systems

- Pidora
- ArchLinux
- RaspBMC
- OpenELEC
