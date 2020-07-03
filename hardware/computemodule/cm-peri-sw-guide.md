# Compute Module Attaching and Enabling Peripherals Guide

** Note that unless explicitly stated otherwise, these instructions will work identically on Compute Module and Compute Module 3 Module+IO board(s). **

## Introduction

This guide is designed to help developers using the Compute Module (and Compute Module 3) get to grips with how to wire up peripherals to the Compute Module pins, and how to make changes to the software to enable these peripherals to work correctly.

The Compute Module (CM) and Compute Module 3 (CM3) contain the Raspberry Pi BCM2835 (or BCM2837 for CM3) system on a chip (SoC) or 'processor', memory, and eMMC. The eMMC is similar to an SD card but is soldered onto the board. Unlike SD cards, the eMMC is specifically designed to be used as a disk and has extra features that make it more reliable in this use case. Most of the pins of the SoC (GPIO, two CSI camera interfaces, two DSI display interfaces, HDMI etc) are freely available and can be wired up as the user sees fit (or, if unused, can usually be left unconnected). The Compute Module is a DDR2 SODIMM form-factor-compatible module, so any DDR2 SODIMM socket should be able to be used (note the pinout is NOT the same as an actual SODIMM memory module).

To use the Compute Module, a user needs to design a (relatively simple) 'motherboard' which can provide power to the Compute Module (3.3V and 1.8V at minimum), and which connects the pins to the required peripherals for the user's application.

Raspberry Pi provides a minimal motherboard for the Compute Module (called the Compute Module IO Board, or CMIO Board) which powers the module, brings out the GPIO to pin headers, and brings the camera and display interfaces out to FFC connectors. It also provides HDMI, USB, and an 'ACT' LED, as well as the ability to program the eMMC of a module via USB from a PC or Raspberry Pi.

This guide first explains the boot process and how Device Tree is used to describe attached hardware; these are essential things to understand when designing with the Compute Module. It then provides a worked example of attaching an I2C and an SPI peripheral to a CMIO (or CMIO V3 for CM3) Board and creating the Device Tree files necessary to make both peripherals work under Linux, starting from a vanilla Raspberry Pi OS image.

## BCM283x GPIOs

BCM283x has three banks of General-Purpose Input/Output (GPIO) pins: 28 pins on Bank 0, 18 pins on Bank 1, and 8 pins on Bank 2, making 54 pins in total. These pins can be used as true GPIO  pins, i.e. software can set them as inputs or outputs, read and/or set state, and use them as interrupts. They also can be set to 'alternate functions' such as I2C, SPI, I2S, UART, SD card, and others.

On a Compute Module, both Bank 0 and Bank 1 are free to use. Bank 2 is used for eMMC and HDMI hot plug detect and ACT LED / USB boot control.

It is useful on a running system to look at the state of each of the GPIO pins (what function they are set to, and the voltage level at the pin) so that you can see if the system is set up as expected. This is particularly helpful if you want to see if a Device Tree is working as expected, or to get a look at the pin states during hardware debug.

Raspberry Pi provides the `raspi-gpio` package which is a tool for hacking and debugging GPIO (NOTE: you need to run it as root).
To install `raspi-gpio`:
```
sudo apt install raspi-gpio
```

If `apt` can't find the `raspi-gpio` package, you will need to do an update first:
```
sudo apt update
```

To get help on `raspi-gpio`, run it with the `help` argument:
```
sudo raspi-gpio help
```

For example, to see the current function and level of all GPIO pins use:
```
sudo raspi-gpio get
```

Note that `raspi-gpio` can be used with the `funcs` argument to get a list of all supported GPIO functions per pin. It will print out a table in CSV format. The idea is to pipe the table to a `.csv` file and then load this file using e.g. Excel:
```
sudo raspi-gpio funcs > gpio-funcs.csv
```

## BCM283x Boot Process

BCM283x devices consist of a VideoCore GPU and ARM CPU cores. The GPU is in fact a system consisting of a DSP processor and hardware accelerators for imaging, video encode and decode, 3D graphics, and image compositing.

In BCM283x devices, it is the DSP core in the GPU that boots first. It is responsible for general setup and housekeeping before booting up the main ARM processor(s).

The BCM283x devices as used on Raspberry Pi and Compute Module boards have a three-stage boot process:

1. The GPU DSP comes out of reset and executes code from a small internal ROM (the boot ROM). The sole purpose of this code is to load a second stage boot loader via one of the external interfaces. On a Raspberry Pi or Compute Module, this code first looks for a second stage boot loader on the SD card (eMMC); it expects this to be called `bootcode.bin` and to be on the first partition (which must be FAT32). If no SD card is found or `bootcode.bin` is not found, the Boot ROM sits and waits in 'USB boot' mode, waiting for a host to give it a second stage boot loader via the USB interface.

2. The second stage boot loader (`bootcode.bin` on the sdcard or `usbbootcode.bin` for usb boot) is responsible for setting up the LPDDR2 SDRAM interface and various other critical system functions and then loading and executing the main GPU firmware (called `start.elf`, again on the primary SD card partition).

3. `start.elf` takes over and is responsible for further system setup and booting up the ARM processor subsystem, and contains the firmware that runs on the various parts of the GPU. It first reads `dt-blob.bin` to determine initial GPIO pin states and GPU-specific interfaces and clocks, then parses `config.txt`. It then loads an ARM device tree file (e.g. `bcm2708-rpi-cm.dtb` for a Compute Module) and any device tree overlays specified in `config.txt` before starting the ARM subsystem and passing the device tree data to the booting Linux kernel.

## Device Tree

[Device Tree](http://www.devicetree.org/) is a special way of encoding all the information about the hardware attached to a system (and consequently required drivers).

On a Pi or Compute Module there are several files in the first FAT partition of the SD/eMMC that are binary 'Device Tree' files. These binary files (usually with extension `.dtb`) are compiled from human readable text descriptions (usually files with extension `.dts`) by the Device Tree compiler.

On a standard Raspberry Pi OS image in the first (FAT) partition you will find two different types of device tree files, one is used by the GPU only and the rest are standard ARM device tree files for each of the BCM283x based Pi products:

* `dt-blob.bin` (used by the GPU)
* `bcm2708-rpi-b.dtb` (Used for Pi model A and B)
* `bcm2708-rpi-b-plus.dtb` (Used for Pi model B+ and A+)
* `bcm2709-rpi-2-b.dtb` (Used for Pi 2 model B)
* `bcm2710-rpi-3-b.dtb` (Used for Pi 3 model B)
* `bcm2708-rpi-cm.dtb` (Used for Pi Compute Module)
* `bcm2710-rpi-cm3.dtb` (Used for Pi Compute Module 3)

NOTE `dt-blob.bin` by default does not exist as there is a 'default' version compiled into `start.elf`, but for Compute Module projects it will often be necessary to provide a `dt-blob.bin` (which overrides the default built-in file).

Note that `dt-blob.bin` is in compiled device tree format, but is only read by the GPU firmware to set up functions exclusive to the GPU - see below.

A guide to creating dt-blob.bin is [here](../../configuration/pin-configuration.md).
A comprehensive guide to the Linux Device Tree for Raspberry Pi is [here](../../configuration/device-tree.md).

During boot, the user can specify a specific ARM device tree to use via the `device_tree` parameter in `config.txt`, for example adding the line `device_tree=mydt.dtb` to `config.txt` where `mydt.dtb` is the dtb file to load instead of one of the standard ARM dtb files. While a user can create a full device tree for their Compute Module product, the recommended way to add hardware is to use overlays (see next section).

In addition to loading an ARM dtb, `start.elf` supports loading additional Device Tree 'overlays' via the `dtoverlay` parameter in `config.txt`, for example adding as many `dtoverlay=myoverlay` lines as required as overlays to `config.txt`, noting that overlays live in `/overlays` and are suffixed `-overlay.dtb` e.g. `/overlays/myoverlay-overlay.dtb`. Overlays are merged with the base dtb file before the data is passed to the Linux kernel when it starts.

Overlays are used to add data to the base dtb that (nominally) describes non board-specific hardware. This includes GPIO pins used and their function, as well as the device(s) attached, so that the correct drivers can be loaded. The convention is that on a Raspberry Pi, all hardware attached to the Bank0 GPIOs (the GPIO header) should be described using an overlay. On a Compute Module all hardware attached to the Bank0 and Bank1 GPIOs should be described in an overlay file. You don't have to follow these conventions: you can roll all the information into one single dtb file, as previously described, replacing `bcm2708-rpi-cm.dtb`. However, following the conventions means that you can use a 'standard' Raspberry Pi OS release, with its standard base dtb and all the product-specific information contained in a separate overlay. Occasionally the base dtb might change - usually in a way that will not break overlays - which is why using an overlay is suggested.

## dt-blob.bin

When `start.elf` runs, it first reads something called `dt-blob.bin`. This is a special form of Device Tree blob which tells the GPU how to (initially) set up the GPIO pin states, and also any information about GPIOs/peripherals that are controlled (owned) by the GPU, rather than being used via Linux on the ARM. For example, the Raspberry Pi Camera peripheral is managed by the GPU, and the GPU needs exclusive access to an I2C interface to talk to it, as well as a couple of control pins. I2C0 on most Pi Boards and Compute Modules is nominally reserved for exclusive GPU use. The information on which GPIO pins the GPU should use for I2C0, and to control the camera functions, comes from `dt-blob.bin`. 

NOTE: the `start.elf` firmware has a 'built-in' default `dt-blob.bin` which is used if no `dt-blob.bin` is found on the root of the first FAT partition. Most Compute Module projects will want to provide their own custom `dt-blob.bin`. Note that `dt-blob.bin` specifies which pin is for HDMI hot plug detect, although this should never change on Compute Module. It can also be used to set up a GPIO as a GPCLK output, and specify an ACT LED that the GPU can use while booting. Other functions may be added in future. For information on `dt-blob.bin` see [here](../../configuration/pin-configuration.md).

[minimal-cm-dt-blob.dts](minimal-cm-dt-blob.dts) is an example `.dts` device tree file that sets up the HDMI hot plug detect and ACT LED and sets all other GPIOs to be inputs with default pulls.

To compile the `minimal-cm-dt-blob.dts` to `dt-blob.bin` use the Device Tree Compiler `dtc`:
```
dtc -I dts -O dtb -o dt-blob.bin minimal-cm-dt-blob.dts
```

## ARM Linux Device Tree

After `start.elf` has read `dt-blob.bin` and set up the initial pin states and clocks, it reads `config.txt` which contains many other options for system setup (see [here](../../configuration/config-txt/README.md) for a comprehensive guide).

After reading `config.txt` another device tree file specific to the board the hardware is running on is read: this is `bcm2708-rpi-cm.dtb` for a Compute Module, or `bcm2710-rpi-cm.dtb` for CM3. This file is a standard ARM Linux device tree file, which details how hardware is attached to the processor: what peripheral devices exist in the SoC and where, which GPIOs are used, what functions those GPIOs have, and what physical devices are connected. This file will set up the GPIOs appropriately, overwriting the pin state set up in `dt-blob.bin` if it is different. It will also try to load driver(s) for the specific device(s).

Although the `bcm2708-rpi-cm.dtb` file can be used to load all attached devices, the recommendation for Compute Module users is to leave this file alone. Instead, use the one supplied in the standard Raspberry Pi OS software image, and add devices using a custom 'overlay' file as previously described. The `bcm2708-rpi-cm.dtb` file contains (disabled) entries for the various peripherals (I2C, SPI, I2S etc.) and no GPIO pin definitions, apart from the eMMC/SD Card peripheral which has GPIO defs and is enabled, because it is always on the same pins. The idea is that the separate overlay file will enable the required interfaces, describe the pins used, and also describe the required drivers. The `start.elf` firmware will read and merge the `bcm2708-rpi-cm.dtb` with the overlay data before giving the merged device tree to the Linux kernel as it boots up.

## Device Tree Source and Compilation

The Raspberry Pi OS image provides compiled dtb files, but where are the source dts files? They live in the Raspberry Pi Linux kernel branch, on [GitHub](https://github.com/raspberrypi/linux). Look in the `arch/arm/boot/dts` folder.

Some default overlay dts files live in `arch/arm/boot/dts/overlays`. Corresponding overlays for standard hardware that can be attached to a **Raspberry Pi** in the Raspberry Pi OS image are on the FAT partition in the `/overlays` directory. Note that these assume certain pins on BANK0, as they are for use on a Raspberry Pi. In general, use the source of these standard overlays as a guide to creating your own, unless you are using the same GPIO pins as you would be using if the hardware was plugged into the GPIO header of a Raspberry Pi.

Compiling these dts files to dtb files requires an up-to-date version of the Device Tree compiler `dtc`. More information can be found [here](../../configuration/device-tree.md), but the easy way to install an appropriate version on a Pi is to run:
```
sudo apt install device-tree-compiler
```

If you are building your own kernel then the build host also gets a version in `scripts/dtc`. You can arrange for your overlays to be built automatically by adding them to `Makefile` in `arch/arm/boot/dts/overlays`, and using the 'dtbs' make target.

## Device Tree Debugging

When the Linux kernel is booted on the ARM core(s), the GPU provides it with a fully assembled device tree, assembled from the base dts and any overlays. This full tree is available via the Linux proc interface in `/proc/device-tree`, where nodes become directories and properties become files.

You can use `dtc` to write this out as a human readable dts file for debugging. You can see the fully assembled device tree, which is often very useful:
```
dtc -I fs -O dts -o proc-dt.dts /proc/device-tree
```

As previously explained in the GPIO section, it is also very useful to use `raspi-gpio` to look at the setup of the GPIO pins to check that they are as you expect:
```
raspi-gpio get
```

If something seems to be going awry, useful information can also be found by dumping the GPU log messages:
```
sudo vcdbg log msg
```

You can include more diagnostics in the output by adding `dtdebug=1` to `config.txt`.

## Getting Help

Please use the [Device Tree subforum](https://www.raspberrypi.org/forums/viewforum.php?f=107) on the Raspberry Pi forums to ask Device Tree related questions.

## Examples

For these simple examples I used a CMIO board with peripherals attached via jumper wires.

For each of the examples we assume a CM+CMIO or CM3+CMIO3 board with a clean install of the latest Raspberry Pi OS Lite version on the CM. See instructions [here](cm-emmc-flashing.md).

The examples here require internet connectivity, so a USB hub plus keyboard plus wireless LAN or Ethernet dongle plugged into the CMIO USB port is recommended.

Please post any issues, bugs or questions on the Raspberry Pi [Device Tree subforum](https://www.raspberrypi.org/forums/viewforum.php?f=107).

## Example 1 - attaching an I2C RTC to BANK1 pins

In this simple example we wire an NXP PCF8523 real time clock (RTC) to the CMIO board BANK1 GPIO pins: 3V3, GND, I2C1_SDA on GPIO44 and I2C1_SCL on GPIO45.

Download [minimal-cm-dt-blob.dts](minimal-cm-dt-blob.dts) and copy it to the SD card FAT partition, located in `/boot` when the CM has booted.

Edit `minimal-cm-dt-blob.dts` and change the pin states of GPIO44 and 45 to be I2C1 with pull-ups:
```
sudo nano /boot/minimal-cm-dt-blob.dts
```

Change lines:
```
pin@p44 { function = "input"; termination = "pull_down"; }; // DEFAULT STATE WAS INPUT NO PULL
pin@p45 { function = "input"; termination = "pull_down"; }; // DEFAULT STATE WAS INPUT NO PULL
```

to:
```
pin@p44 { function = "i2c1"; termination = "pull_up"; }; // SDA1
pin@p45 { function = "i2c1"; termination = "pull_up"; }; // SCL1
```

NOTE: we could use this `dt-blob.dts` with no changes The Linux Device Tree will (re)configure these pins during Linux kernel boot when the specific drivers are loaded, so it is up to you whether you modify `dt-blob.dts`. I like to configure `dt-blob.dts` to what I expect the final GPIOs to be, as they are then set to their final state as soon as possible during the GPU boot stage, but this is not strictly necessary. You may find that in some cases you do need pins to be configured at GPU boot time, so they are in a specific state when Linux drivers are loaded. For example, a reset line may need to be held in the correct orientation.

Compile `dt-blob.bin`:
```
sudo dtc -I dts -O dtb -o /boot/dt-blob.bin /boot/minimal-cm-dt-blob.dts
```

Grab [example1-overlay.dts](example1-overlay.dts) and put it in `/boot` then compile it:
```
sudo dtc -@ -I dts -O dtb -o /boot/overlays/example1.dtbo /boot/example1-overlay.dts
```
Note the '-@' in the `dtc` command line. This is necessary if you are compiling dts files with external references, as overlays tend to be.

Edit `/boot/config.txt` and add the line:
```
dtoverlay=example1
```

Now save and reboot.

Once rebooted, you should see an rtc0 entry in /dev. Running:
```
sudo hwclock
```

will return with the hardware clock time, and not an error.

## Example 2 - Attaching an ENC28J60 SPI Ethernet Controller on BANK0

In this example we use one of the already available overlays in /boot/overlays to add an ENC28J60 SPI Ethernet controller to BANK0. The Ethernet controller is connected to SPI pins CE0, MISO, MOSI and SCLK (GPIO8-11 respectively), as well as GPIO25 for a falling edge interrupt, and of course GND and 3V3.

In this example we won't change `dt-blob.bin`, although of course you can if you wish. We should see that Linux Device Tree correctly sets up the pins.

Edit `/boot/config.txt` and add the line:
```
dtoverlay=enc28j60
```

Now save and reboot.

Once rebooted you should see, as before, an rtc0 entry in /dev. Running:
```
sudo hwclock
```

will return with the hardware clock time, and not an error.

You should also have Ethernet connectivity:
```
ping 8.8.8.8
```

should work.

finally running:
```
sudo raspi-gpio get
```

should show that GPIO8-11 have changed to ALT0 (SPI) functions.

## Attaching a camera or cameras
To attach a camera or cameras see the documentation [here](cmio-camera.md)
