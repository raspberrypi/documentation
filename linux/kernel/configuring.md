# Configuring the kernel

The Linux kernel is highly configurable; advanced users may wish to modify the default configuration to customise it to their needs, such as enabling a new or experimental network protocol, or enabling support for new hardware.

Configuration is most commonly done through the `make menuconfig` interface. Alternatively, you can modify your `.config` file manually, but this can be more difficult for new users.

## Preparing to configure the kernel

The `menuconfig` tool requires the `ncurses` development headers to compile properly. These can be installed with the following command:

```
$ sudo apt install libncurses5-dev
```

You'll also need to download and prepare your kernel sources, as described in the [build guide](building.md). In particular, ensure you have installed the default configuration.

For all models of Raspberry Pi 1 (includes Compute Module and Pi Zero):

```
$ KERNEL=kernel
$ make bcmrpi_defconfig
```

If you're cross-compiling, the second line should be:

```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig
```

For all models of Raspberry Pi 2/3 (includes 3B+, 3A+ and Compute Module 3):

```
$ KERNEL=kernel7
$ make bcm2709_defconfig
```

If you're cross-compiling, the second line should be:

```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig
```

## Using menuconfig

Once you've got everything set up and ready to go, you can compile and run the `menuconfig` utility as follows:

```
$ make menuconfig
```

If you're cross-compiling,:

```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
```

The `menuconfig` utility has simple keyboard navigation. After a brief compilation, you'll be presented with a list of submenus containing all the options you can configure; there's a lot, so take your time to read through them and get acquainted.

Use the arrow keys to navigate, the Enter key to enter a submenu (indicated by `--->`), Escape twice to go up a level or exit, and the space bar to cycle the state of an option. Some options have multiple choices, in which case they'll appear as a submenu and the Enter key will select an option. You can press `h` on most entries to get help about that specific option or menu.

Resist the temptation to enable or disable a lot of things on your first attempt; it's relatively easy to break your configuration, so start small and get comfortable with the configuration and build process.

## Exiting, saving, and loading configurations

Once you're done making the changes you want, press Escape until you're prompted to save your new configuration. By default, this will save to the `.config` file. You can save and load configurations by copying this file around.
