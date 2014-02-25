# Kernel building
The Raspberry Pi kernel is stored in github and can be viewed by going to https://github.com/raspberrypi/linux it follows behind the main linux kernel https://www.kernel.org/

The main linux kernel is a continuously moving kernel, we take longterm releases of the kernel (those are mentioned on the front page) and integrate the changes into the Raspberry Pi kernel.  Then create a 'next' branch which contains that somewhat unstable port of the kernel, after some time of testing and discussion we push this to the main branch.

There are two main methods for building the kernel, locally on a Raspberry Pi (be prepared to wait!) or cross compiled (much quicker but requires more setup)

## Local building

On a Raspberry Pi first install the latest version of [Raspbian](http://www.raspberrypi.org/downloads) from the downloads page. Then boot your Pi, plug in ethernet (to give you access to the sources) and log in.
```
$ git clone --depth=1 https://github.com/raspberrypi/linux

$ make bcmrpi_defconfig
$ make
$ make modules
$ sudo make modules_install
```

## Links

Building / cross compiling on/for other operating systems
* Pidora
* ArchLinux
* RaspBMC
* OpenElec
