# Kernel building

The default compilers and linkers that come with an OS are configured to build executables to run on that OS - they are native tools - but that doesn't have to be the case. A cross-compiler is configured to build code for a target other than the one running the build process, and using it is called cross-compilation.

Cross-compilation of the Raspberry Pi kernel is useful for two reasons:

 * it allows a 64-bit kernel to be built using a 32-bit OS, and vice versa, and
 * even a modest laptop can cross-compile a Pi kernel significantly faster than the Pi itself.

The instructions below are divided into native builds and cross-compilation; choose the section appropriate for your situation - although there are many common steps between the two, there are also some important differences.

## Local building

On a Raspberry Pi, first install the latest version of [Raspberry Pi OS](https://www.raspberrypi.org/downloads/). Then boot your Pi, plug in Ethernet to give you access to the sources, and log in.

First install Git and the build dependencies:

```bash
sudo apt install git bc bison flex libssl-dev make
```

Next get the sources, which will take some time:

```bash
git clone --depth=1 https://github.com/raspberrypi/linux
```

<a name="choosing_sources"></a>

### Choosing sources

The `git clone` command above will download the current active branch (the one we are building Raspberry Pi OS images from) without any history. Omitting the `--depth=1` will download the entire repository, including the full history of all branches, but this takes much longer and occupies much more storage.

To download a different branch (again with no history), use the `--branch` option:

```bash
git clone --depth=1 --branch <branch> https://github.com/raspberrypi/linux
```

where `<branch>` is the name of the branch that you wish to download.

Refer to the [original GitHub repository](https://github.com/raspberrypi/linux) for information about the available branches.

### Kernel configuration

Configure the kernel; as well as the default configuration, you may wish to [configure your kernel in more detail](configuring.md) or [apply patches from another source](patching.md), to add or remove required functionality.

<a name="default_configuration"></a>
#### Apply the default configuration

First, prepare the default configuration by running the following commands, depending on your Raspberry Pi version:

##### Raspberry Pi 1, Pi Zero, Pi Zero W, and Compute Module default build configuration

```bash
cd linux
KERNEL=kernel
make bcmrpi_defconfig
```

##### Raspberry Pi 2, Pi 3, Pi 3+, and Compute Module 3 default build configuration

```bash
cd linux
KERNEL=kernel7
make bcm2709_defconfig
```

##### Raspberry Pi 4 default build configuration

```bash
cd linux
KERNEL=kernel7l
make bcm2711_defconfig
```

#### Customising the Kernel version using LOCALVERSION

In addition to your kernel configuration changes, you may wish to adjust the `LOCALVERSION` to ensure your new kernel does not receive the same version string as the upstream kernel. This both clarifies you are running your own kernel in the output of `uname` and ensures existing modules in `/lib/modules` are not overwritten.

To do so, change the following line in `.config`:
```
CONFIG_LOCALVERSION="-v7l-MY_CUSTOM_KERNEL"
```
You can also change that setting graphically as shown in [the kernel configuration instructions](configuring.md). It is located in "General setup" => "Local version - append to kernel release".

### Building

Build and install the kernel, modules, and Device Tree blobs; this step can take a **long** time depending on the Pi model in use:

```bash
make -j4 zImage modules dtbs
sudo make modules_install
sudo cp arch/arm/boot/dts/*.dtb /boot/
sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
sudo cp arch/arm/boot/zImage /boot/$KERNEL.img
```

**Note**: On a Raspberry Pi 2/3/4, the `-j4` flag splits the work between all four cores, speeding up compilation significantly.

## Cross-compiling 

First, you will need a suitable Linux cross-compilation host. We tend to use Ubuntu; since Raspberry Pi OS is 
also a Debian distribution, it means many aspects are similar, such as the command lines.

You can either do this using VirtualBox (or VMWare) on Windows, or install it directly onto your computer. For reference, you can follow instructions online [at Wikihow](http://www.wikihow.com/Install-Ubuntu-on-VirtualBox).

### Install required dependencies and toolchain

To build the sources for cross-compilation, make sure you have the dependencies needed on your machine by executing:
```bash
sudo apt install git bc bison flex libssl-dev make libc6-dev libncurses5-dev
```

If you find you need other things, please submit a pull request to change the documentation.

#### Install the 32-bit toolchain for a 32-bit kernel
```bash
sudo apt install crossbuild-essential-armhf
```

#### Or, install the 64-bit toolchain for a 64-bit kernel
```bash
sudo apt install crossbuild-essential-arm64
```

### Get sources

To download the minimal source tree for the current branch, run:

```bash
git clone --depth=1 https://github.com/raspberrypi/linux
```

See [**Choosing sources**](#choosing_sources) above for instructions on how to choose a different branch.

### Build sources

Enter the following commands to build the sources and Device Tree files:

#### 32-bit configs
For Pi 1, Pi Zero, Pi Zero W, or Compute Module:

```bash
cd linux
KERNEL=kernel
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig
```

For Pi 2, Pi 3, Pi 3+, or Compute Module 3:

```bash
cd linux
KERNEL=kernel7
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig
```

For Raspberry Pi 4:

```bash
cd linux
KERNEL=kernel7l
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2711_defconfig
```

#### 64-bit configs
For Pi 3, Pi 3+ or Compute Module 3:
```bash
cd linux
KERNEL=kernel8
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- bcmrpi3_defconfig
```

For Raspberry Pi 4:
```bash
cd linux
KERNEL=kernel8
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- bcm2711_defconfig
```

#### Build with configs

**Note**: To speed up compilation on multiprocessor systems, and get some improvement on single processor ones, use `-j n`, where n is the number of processors * 1.5. Alternatively, feel free to experiment and see what works!

##### For all 32-bit builds
```bash
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs
```

##### For all 64-bit builds
**Note**: Note the difference between Image target between 32 and 64-bit.
```bash
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image modules dtbs
```

### Install directly onto the SD card

Having built the kernel, you need to copy it onto your Raspberry Pi and install the modules; this is best done directly using an SD card reader.

First, use `lsblk` before and after plugging in your SD card to identify it. You should end up with something like this:

```
sdb
   sdb1
   sdb2
```

with `sdb1` being the FAT (boot) partition, and `sdb2` being the ext4 filesystem (root) partition.

If it's a NOOBS card, you should see something like this:

```
sdb
  sdb1
  sdb2
  sdb5
  sdb6
  sdb7
```

with `sdb6` being the FAT (boot) partition, and `sdb7` being the ext4 filesystem (root) partition.

Mount these first, adjusting the partition numbers for NOOBS cards (as necessary):

```bash
mkdir mnt
mkdir mnt/fat32
mkdir mnt/ext4
sudo mount /dev/sdb6 mnt/fat32
sudo mount /dev/sdb7 mnt/ext4
```


Next, install the kernel modules onto the SD card:

#### For 32-bit
```bash
sudo env PATH=$PATH make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install
```

#### For 64-bit
```bash
sudo env PATH=$PATH make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=mnt/ext4 modules_install
```

Finally, copy the kernel and Device Tree blobs onto the SD card, making sure to back up your old kernel:

#### For 32-bit

```bash
sudo cp mnt/fat32/$KERNEL.img mnt/fat32/$KERNEL-backup.img
sudo cp arch/arm/boot/zImage mnt/fat32/$KERNEL.img
sudo cp arch/arm/boot/dts/*.dtb mnt/fat32/
sudo cp arch/arm/boot/dts/overlays/*.dtb* mnt/fat32/overlays/
sudo cp arch/arm/boot/dts/overlays/README mnt/fat32/overlays/
sudo umount mnt/fat32
sudo umount mnt/ext4
```

#### For 64-bit

```bash
sudo cp mnt/fat32/$KERNEL.img mnt/fat32/$KERNEL-backup.img
sudo cp arch/arm64/boot/Image mnt/fat32/$KERNEL.img
sudo cp arch/arm64/boot/dts/broadcom/*.dtb mnt/fat32/
sudo cp arch/arm64/boot/dts/overlays/*.dtb* mnt/fat32/overlays/
sudo cp arch/arm64/boot/dts/overlays/README mnt/fat32/overlays/
sudo umount mnt/fat32
sudo umount mnt/ext4
```

Another option is to copy the kernel into the same place, but with a different filename - for instance, kernel-myconfig.img - rather than overwriting the kernel.img file. You can then edit the config.txt file to select the kernel that the Pi will boot into:

```
kernel=kernel-myconfig.img
```

This has the advantage of keeping your kernel separate from the kernel image managed by the system and any automatic update tools, and allowing you to easily revert to a stock kernel in the event that your kernel cannot boot.

Finally, plug the card into the Pi and boot it!
