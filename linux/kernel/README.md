# Kernel

The Raspberry Pi kernel is stored in GitHub and can be viewed at [github.com/raspberrypi/linux](https://github.com/raspberrypi/linux); it follows behind the main [Linux kernel](https://github.com/torvalds/linux).

The main Linux kernel is continuously updating; we take long-term releases of the kernel, which are mentioned on the front page, and integrate the changes into the Raspberry Pi kernel. We then create a 'next' branch which contains an unstable port of the kernel; after extensive testing and discussion, we push this to the main branch.

- [Updating your kernel](updating.md)
- [Building a new kernel](building.md)
- [Configuring the kernel](configuring.md)
- [Applying patches to the kernel](patching.md)
- [Getting the kernel headers](headers.md)

## Getting your code into the kernel

There are many reasons you may want to put something into the kernel:

- You've written some Raspberry Pi-specific code that you want everyone to benefit from
- You've written a generic Linux kernel driver for a device and want everyone to use it
- You've fixed a generic kernel bug
- You've fixed a Raspberry Pi-specific kernel bug

Initially, you should fork the Linux repository and clone that on your build system; this can be either on the Raspberry Pi or on a Linux machine you're using for cross-compiling. You can then make your changes, test them, and commit them into your fork.

Next, depending upon whether the code is Raspberry Pi-specific or not:

- For Pi-specific changes or bug fixes, submit a pull request to the kernel.

- For general Linux kernel changes (i.e. a new driver), these need to be submitted upstream first. Once they've been submitted upstream and accepted, submit the pull request and we'll receive it.
