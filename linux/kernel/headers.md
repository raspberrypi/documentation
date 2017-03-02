# Kernel Headers

If you are compiling a kernel module or similar, you will need the Linux Kernel headers. These provide various function and structure definitions required when compiling code that interfaces with the kernel.

If you have cloned the entire kernel from github, then the headers are already included in the source tree, but if you don't need all the extra files then it is possible to only install the kernel headers from the Raspbian repo

```
sudo apt-get install raspberrypi-kernel-headers
```
Note that is can take quite a while for this command to complete as it installs a lot of small files, and there is no progress indicator.

When a new kernel release is made, you need the headers that match that kernel version, and it can take some time (weeks) for the repo to be updated to reflect the latest kernel version. In that case the best approach is to clone the kernel as described in the [Build Section](building.md).

