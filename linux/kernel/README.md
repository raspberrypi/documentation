#Kernel

The Raspberry Pi kernel is stored in github and can be viewed by going to https://github.com/raspberrypi/linux it follows behind the main linux kernel https://www.kernel.org/

The main linux kernel is a continuously moving kernel, we take longterm releases of the kernel (those are mentioned on the front page) and integrate the changes into the Raspberry Pi kernel. Then create a 'next' branch which contains that somewhat unstable port of the kernel, after some time of testing and discussion we push this to the main branch.

* [Updating your kernel](updating.md)
* [Building a new kernel](building.md)
* [Configuring the kernel](configuring.md)
* [Getting the kernel headers](headers.md)

##Getting your code into the kernel

There are many reasons you may want to put something into the kernel:

* You've written some Raspberry Pi specific code that you want everyone to benefit from
* You've written a generic Linux kernel driver for device X and want everyone to use it
* You've fixed a generic kernel bug
* You've fixed a Raspberry Pi specific kernel bug

Initially you should fork the linux repository and clone that on your build system (can be either on the Raspberry Pi or on a linux box your cross compiling on).  Then make your changes, test them and commit them into your fork.

Next, it depends upon whether the code is Raspberry Pi specific or not:

For Pi specific changes / bug fixes submit a pull request to the kernel
For general linux kernel changes (i.e. a new driver) these need to be submitted upstream first.  Once they've been submitted upstream and accepted submit the pull request and we'll take it.
