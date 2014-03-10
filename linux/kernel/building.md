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

Build the kernel

```
$ make bcmrpi_defconfig
$ make
$ make modules
$ sudo make modules_install
```

## Links

Building / cross compiling on/for other operating systems
- Pidora
- ArchLinux
- RaspBMC
- OpenELEC
