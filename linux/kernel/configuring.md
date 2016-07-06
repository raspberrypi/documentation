# Configuring the Kernel

The Linux Kernel is highly configurable and advanced users may wish to modify the default configuration to customize it to their needs, for instance to enable a new or experimental network protocol or to enable support for new hardware.

Configuration is most commonly done through the `make menuconfig` interface. Alternatively, you can modify your `.config` file manually, but this can be more difficult for new users.

## Preparing to configure the kernel

The menuconfig tool requires the ncurses development headers to compile properly. These can be installed with the following command:

```
$ sudo apt-get install libncurses5-dev
```

You will also need to download and prepare your kernel sources as described in the [build guide](building.md). In particular ensure you have installed the default configuration for the Raspberry Pi with the following command:

```
$ make bcmrpi_defconfig
```

## Using menuconfig

Once you've got everything set up and ready to go, you can compile and run the menuconfig utility as follows:

```
$ make menuconfig
```

The menuconfig utility has simple keyboard navigation. After a brief compilation you'll be presented with a list of submenus containing all the options you can configure; there's a lot, so take your time to read through some and get acquainted.

Use the arrow keys to navigate, the enter key to enter a submenu (indicated by `--->`), escape twice to go up a level or exit, and the space bar to cycle the state of an option. Some options have multiple choices, in which case they will appear as a submenu and the enter key will select an option. You can press `h` on most entries to get help about that specific option or menu.

Resist the temptation to enable or disable a lot of things on your first attempt - it is relatively easy to break your configuration, so start small and get comfortable with the configuration and build process.

## Exiting, saving and loading configurations

Once you're done making the changes you want to make, press escape until you are prompted to save your new configuration. By default this will save to the .config file. You can save and load configurations by copying this file around.

