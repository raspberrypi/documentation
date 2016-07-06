# Compute Module Attaching & Enabling Peripherals Guide

##Introduction

This guide is designed to help developers using the Compute Module get to grips with how to wire up peripherals to the Compute Module pins, and how to make changes to the software to enable these peripherals to work correctly.

The Compute Module contains the Raspberry Pi BCM2835 System On Chip (SoC) or "processor", memory and eMMC (eMMC is basically like an SD card but soldered onto the board, eMMC (unlike SD cards) is specifically designed to be used as a disk and has extra features that make it more reliable in this use case). Most of the pins of the SoC (GPIO, 2 CSI camera interfaces, 2 DSI display interfaces, HDMI etc.) are freely available and can be wired up as the user sees fit (or if unused can usually be left unconnected). The Compute Module is a DDR2 SODIMM form factor compatible module, so any DDR2 SODIMM socket should be able to be used (note the pinout is NOT the same as an actual SODIMM memory module).

To use the Compute Module a user needs to design a (relatively simple) 'motherboard' that can provide power to the Compute Module (3.3V and 1.8V at minimum) and wires the pins up to the required peripherals for the user's application.

Raspberry Pi provide a minimal motherboard for the Compute Module (called the Compute Module IO Board or CMIO Board) which powers the module, brings out the GPIO to pin headers, brings the camera and display interfaces out to FFC connectors, provides HDMI, USB and an 'ACT' LED as well as the ability to program the eMMC of a module via USB from a PC or Raspberry Pi.

This guide first explains the boot process and how Device Tree is used to describe attached hardware (which are essential things to understand when designing with the Compute Module). It then provides a worked example of attaching an I2C and an SPI peripheral to a CMIO Board and creating the Device Tree files necessary to make both peripherals work under Linux (starting from a vanilla Raspbian OS image).

Note that using Device Tree is the officially supported method of doing things (for both a Compute Module and a Raspberry Pi), you *can* at the moment turn off device tree in the kernel altogether but we won't be providing support for this.

##BCM283x GPIOs

BCM283x has 3 banks of General Purpose Input Output (GPIO) pins (28 pins on Bank0, 18 pins on Bank1 and 8 pins on Bank2; 54 pins in total). These pins can be used as true GPIO (i.e. software can set them as inputs or outputs, read and/or set state and use them as interrupts) but also can be set to 'alternate functions' such as I2C, SPI, I2S, UART, SD card and others.

On a Compute Module both Bank0 and Bank1 are free to use with Bank2 used for eMMC and HDMI hot plug detect and ACT LED / USB boot control.

It is useful on a running system to look at the state of each of the GPIO pins (what function they are set to, and the voltage level at the pin) - so that one can see if the system is set up as expected (this is particularly useful to see if a Device Tree is working as expected or to get a look at the pin states during hardware debug).

Raspberry Pi provide the `raspi-gpio` package which is a tool for hacking / debugging GPIO (NOTE you need to run it as root).
To install `raspi-gpio`:
```
sudo apt-get install raspi-gpio
```

If `apt-get` can't find the `raspi-gpio` package you need to do an update first:
```
sudo apt-get update
```

To get help on `raspi-gpio` run it with the `help` argument:
```
sudo raspi-gpio help
```

For example to see the current function and level of all GPIO pins use:
```
sudo raspi-gpio get
```

Note `raspi-gpio` can be used with the `funcs` argument to get a list of all supported GPIO functions per pin, it will print out a table in CSV format. The idea is to pipe the table to a `.csv` file and then load this file using e.g. Excel:
```
sudo raspi-gpio funcs > gpio-funcs.csv
```

##BCM283x Boot Process

BCM283x devices consist of a VideoCore 'GPU' and ARM 'CPU' cores. The GPU is in fact a system consisting of a DSP processor and hardware accelerators for imaging, video encode and decode, 3D graphics and image compositing.

In BCM283x devices it is the DSP core in the GPU that boots first and is responsible for general setup and housekeeping before booting up the main ARM processor(s).

The BCM283x devices as used on Raspberry Pi and Compute Module boards have a 3 stage boot process:

1. The GPU DSP comes out of reset and executes code from a small internal ROM (the Boot ROM). The sole purpose of this code is to load a 'second stage' boot loader via one of the external interfaces. On a Pi or Compute Module this code first looks for a 2nd stage boot loader on the SD card (eMMC) and expects it to be called `bootcode.bin` and be on the first partition (which must be FAT32). If no SD card is found or no `bootcode.bin` is found, the Boot ROM sits and waits in 'USB boot' mode, waiting for a host to give it a second stage boot loader via the USB interface.

2. The second stage boot loader (`bootcode.bin` on the sdcard or `usbbootcode.bin` for usb boot) is responsible for setting up the LPDDR2 SDRAM interface and various other critical system funcions and then loading and executing the main GPU firmware (called `start.elf`, again on the primary SD card partition). 

3. `start.elf` takes over and is responsible for further system setup and booting up the ARM processor subsystem, and contains the firmware that runs on the various parts of the GPU. It first reads `dt-blob.bin` to determine initial GPIO pin states and GPU-specific interfaces and clocks, then parses `config.txt`. It then loads an ARM device tree file (e.g. `bcm2708-rpi-cm.dtb` for a Compute Module) and any device tree overlays specified in `config.txt` before starting the ARM subsystem and passing the device tree data to the booting Linux kernel.

##Device Tree

[Device Tree](http://www.devicetree.org/) is a special way of encoding all the information about the hardware attached to a system (and consequently required drivers).

On a Pi or Compute Module there are several files in the first FAT partition of the SD/eMMC that are binary 'Device Tree' files. These binary files (usually with extension `.dtb`) are compiled from human readable text descriptions (usually files with extension `.dts`) by the Device Tree compiler.

On a standard Raspbian image in the first (FAT) partition you will find two different types of device tree files, one is used by the GPU only and the rest are standard ARM device tree files for each of the BCM283x based Pi products:

* `dt-blob.bin` (used by the GPU)
* `bcm2708-rpi-b.dtb` (Used for Pi model A and B)
* `bcm2708-rpi-b-plus.dtb` (Used for Pi model B+ and A+)
* `bcm2709-rpi-2-b.dts` (Used for Pi 2 model B)
* `bcm2708-rpi-cm.dtb` (Used for Pi Compute Module)

NOTE on Raspbian releases 2015-05-05 and earlier `bcm2708-rpi-cm.dtb` is missing, do a `sudo rpi-update` to get it.

NOTE `dt-blob.bin` by default does not exist as there is a 'default' version compiled into `start.elf`, but for most Compute Module projects it will be necessary to provide a `dt-blob.bin` (which overrides the default in-built one).

Note that `dt-blob.bin` is in compiled device tree format, but is only read by the GPU firmware to set up functions exclusive to the GPU - see below.

A guide to creating dt-blob.bin is [here](../../configuration/pin-configuration.md).
A comprehensive guide to the Linux Device Tree for Raspberry Pi is [here](../../configuration/device-tree.md).

During boot, the user can specify a specific ARM device tree to use via the `device_tree` parameter in `config.txt` (e.g. add the line `device_tree=mydt.dtb` to `config.txt` where `mydt.dtb` is the dtb file to load instead of one of the standard ARM dtb files).

In addition to loading an ARM dtb, `start.elf` supports loading aditional Device Tree 'overlays' via the `dtoverlay` parameter in `config.txt`. (e.g. add as many `dtoverlay=myoverlay` lines as required overlays to `config.txt` noting that overlays live in `/overlays` and are suffixed `-overlay.dtb` e.g. `/overlays/myoverlay-overlay.dtb`). Overlays are merged with the base dtb file before the data is passed to the Linux kernel when it starts.

Overlays are used to add data to the base dtb that describes non board-specific hardware, which includes GPIO pins used and their function as well as the device(s) attached (so correct drivers can be loaded). The convention is that on a Raspberry Pi all hardware attached to the Bank0 GPIOs (the GPIO header) should be described using an overlay. On a Compute Module all hardware attached to the Bank0 and Bank1 GPIOs should be described in an overlay file. You don't have to follow these conventions (you can roll all information into one single dtb file, replacing `bcm2708-rpi-cm.dtb`) but following the conventions means that you can use a 'standard' Raspbian release with its standard base dtb and all the product-specific infotmation is contained in a separate overlay. Occasionally the base dtb might change - usually in a way that will not break overlays - which is why using an overlay is suggested.

##dt-blob.bin

When `start.elf` runs it first reads something called `dt-blob.bin` which is a special form of Device Tree blob which tells the GPU how to (initially) set up the GPIO pin states, and also any information about GPIOs/peripherals that are controlled (owned) by the GPU (rather than being used via Linux on the ARM). For example the Raspberry Pi Camera peripheral is managed by the GPU, and the GPU needs exclusive access to an I2C interface to talk to it (I2C0 on most Pi Boards and Compute Module is nominally reserved for exclusive GPU use) as well as a couple of control pins. The information on which GPIO pins the GPU should use for I2C0 and to contol the camera functions comes from `dt-blob.bin`. (NOTE the `start.elf` firmware has a 'built-in' default `dt-blob.bin` which is used if no `dt-blob.bin` is found on the root of the first FAT partition, but most Compute Module projects will want to provide their own custom `dt-blob.bin`). Note that `dt-blob.bin` specifies which pin is for HDMI hot plug detect (though this should never change on Compute Module) and can also be used to set up a GPIO to be a GPCLK output and specify and ACT LED that the GPU can use while booting. Other functions may be added in future. For information on `dt-blob.bin` see [here](../../configuration/pin-configuration.md).

[minimal-cm-dt-blob.dts](minimal-cm-dt-blob.dts) is an example `.dts` device tree file that sets up the HDMI hot plug detect and ACT LED (these are GPIOs 46 and 47 which we state must be used only for these functions on all Compute Module designs) and sets all other GPIOs to be inputs with default pulls.

To compile the `minimal-cm-dt-blob.dts` to `dt-blob.bin` use the Device Tree Compiler `dtc`:
```
dtc -I dts -O dtb -o dt-blob.bin minimal-cm-dt-blob.dts
```

##ARM Linux Device Tree

After `start.elf` has read `dt-blob.bin` and set up the initial pin states and clocks, it reads `config.txt` which contains many other options for system setup (see [here](../../configuration/config-txt.md) for a comprehensive guide).

After reading `config.txt` another device tree file specific to the board the hardware is running on is read; this is `bcm2708-rpi-cm.dtb` for a Compute Module. This file is a standard ARM Linux device tree file, which details how hardware is attached to the processor (what peripheral devices exist in the SoC and where, which GPIOs are used, what functions those GPIOs have, and what physical devices are connected). This file will set up the GPIOs appropriately (it will overwrite pin state set up in `dt-blob.bin` if it is different) and will also try and load driver(s) for the specific device(s).

Although the `bcm2708-rpi-cm.dtb` file can be used to load all attached devices, the recommendation for Compute Moudule users is to leave this file alone (i.e. just use the one supplied in the standard Raspbian software image) and add devices using a custom 'overlay' file as previously described. The `bcm2708-rpi-cm.dtb` file contains (disabled) entries for the various peripherals (such as I2C, SPI, I2S etc.) and no GPIO pin definitions (apart from the eMMC/SD Card peripheral which has GPIO defs and is enabled, because it is always on the same pins). The idea is the separate overlay file will enable the required interfaces, describe the pins used, and also describe the required drivers. The `start.elf` firmware will read and merge the `bcm2708-rpi-cm.dtb` and overlay data before giving the merged device tree to the Linux kernel as it boots up.

##Device Tree Source and Compilation

The Raspbian image provides compiled dtb files, but where are the source dts files? They live in the Raspberry Pi Linux kernel branch, on [GitHub](https://github.com/raspberrypi/linux). Look in the `arch/arm/boot/dts` folder.

Some default overlay dts files live in `arch/arm/boot/dts/overlays` (corresponding overlays for standard hardware that can be attached to a *Raspberry Pi* in the Raspbian image are on the FAT partition in the `/overlays` directory - note these assume certain pins as they are for use on a Raspberry Pi, so in general use the source of these standard overlays as a guide to creating your own unless you are using the exact same GPIO pins as you would be using if the hardware were plugged into the GPIO header of a Raspberry Pi).

To compile these dts files to dtb files requires an up-to-date version of the Device Tree compiler `dtc`. More info can be found [here](../../configuration/device-tree.md), but the easy way to install an appropriate version on a Pi is to run:
```
sudo apt-get install device-tree-compiler
```

If you are building your own kernel then the build host also gets a version in `scripts/dtc`, and you can arrange that your overlays are built automatically by adding them to `Makefile` in `arch/arm/boot/dts/overlays` and using the "dtbs" make target.

##Device Tree Debugging

When the Linux kernel is booted on the ARM core(s) the GPU provides it with a fully assembled device tree (assembled from the base dts and any overlays). This full tree is available via the Linux proc interface in `/proc/device-tree`, where nodes become directories and properties become files.

You can use `dtc` to write this out as a human readable dts file for debugging (you can see the fully assembled device tree which is often very useful):
```
dtc -I fs -O dts -o proc-dt.dts /proc/device-tree
```

As previously explained in the GPIO section it is also very useful to use `raspi-gpio` to look at the setup of the GPIO pins to see if they are as you expect:
```
raspi-gpio get
```

If something seems to be going awry useful information can also be found by dumping the GPU log messages:
```
sudo vcdbg log msg
```

You can include more diagnostics in the output by adding `dtdebug=1` to `config.txt`.

##Getting Help

Please use the [Device Tree subforum](https://www.raspberrypi.org/forums/viewforum.php?f=107) on the Raspberry Pi forums to ask Device Tree related questions.

##Examples

For these simple examples I used a CMIO board with peripherals attached via jumper wires.

For each of the examples we assume a CM+CMIO board with a clean install of the latest Raspbian version on the CM. See instructions [here](cm-emmc-flashing.md).

The examples here require internet connectivity, so a USB hub plus keyboard plus WiFi dongle (or Ethernet dongle) plugged into the CMIO USB port is recommended.

For Raspbian versions 2015-05-05 or earlier do a sudo rpi-update to make sure you have the latest firmware and `bcm2708-rpi-cm.dtb`.

If you suspect any issues or bugs with Device Tree it is always best to try a `sudo rpi-update` to make sure you are using the latest firmware (WARNING if you have edited any of the default .dtb files in `/boot` or `/boot/overlays` these may be overwritten by rpi-update).

Please post any issues / bugs / questions on the Raspberry Pi [Device Tree subforum](https://www.raspberrypi.org/forums/viewforum.php?f=107).

##Example 1 - attaching an I2C RTC

In this simple example we wire an NXP PCF8523 real time clock (RTC) to the CMIO board GPIO pins (3V3, GND, I2C1_SDA on GPIO44 and I2C1_SCL on GPIO45).

Download [minimal-cm-dt-blob.dts](minimal-cm-dt-blob.dts) and copy it to the SD card FAT partition (located in `/boot` when the CM has booted).

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

NOTE we could use this `dt-blob.dts` with no changes, as the Linux Device Tree will (re)configure these pins during Linux kernel boot when the specific drivers are loaded, so it is up to you whether you modify `dt-blob.dts`. I like to configure `dt-blob.dts` to what I expect the final GPIOs to be, as they are then set to their final state as soon as possbile (during the GPU boot stage) but this is not strictly necessary. You may find that in some cases you do need pins to be configured at GPU boot time so they are in a specific state when Linux drivers are loaded (e.g. maybe a reset line needs to be held in the correct orientation).

Compile `dt-blob.bin`:
```
sudo dtc -I dts -O dtb -o /boot/dt-blob.bin /boot/minimal-cm-dt-blob.dts
```

Grab [example1-overlay.dts](example1-overlay.dts) and put it in `/boot` then compile it:
```
sudo dtc -@ -I dts -O dtb -o /boot/overlays/example1-overlay.dtb /boot/example1-overlay.dts
```
Note the '-@' in the `dtc` command line - this is necessary if you are compiling dts files with external references, as overlays tend to be.

Edit `/boot/config.txt` and add the line:
```
dtoverlay=example1
```

Now save and reboot.

Once rebooted you should see an rtc0 entry in /dev and running:
```
sudo hwclock
```

will return with the hardware clock time, and not an error.

##Example 2 - Attaching an ENC28J60 SPI Ethernet Controller

In this example we take the first RTC example and add another peripheral - an ENC28J60 SPI Ethernet Controller. The Ethernet controller is connected to SPI pins CE0, MISO, MOSI and SCLK (GPIO8-11 respectively), as well as GPIO12 for a falling edge interrupt, and of course GND and 3V3.

In this example we won't change `dt-blob.bin` (though of course you can if you wish) and we should see that Linux Device Tree correctly sets up the pins.

Grab [example2-overlay.dts](example2-overlay.dts) and put it in `/boot` then compile it:
```
sudo dtc -@ -I dts -O dtb -o /boot/overlays/example2-overlay.dtb /boot/example2-overlay.dts
```

Edit `/boot/config.txt` and add the line:
```
dtoverlay=example2
```

Now save and reboot.

Once rebooted you should see, as before, an rtc0 entry in /dev and running:
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

##Attaching a camera or cameras
To attach a camera or cameras see the documentation [here](cmio-camera.md)
