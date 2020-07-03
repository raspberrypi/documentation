# Kernel Headers

If you are compiling a kernel module or similar, you will need the Linux Kernel headers. These provide the various function and structure definitions required when compiling code that interfaces with the kernel.

If you have cloned the entire kernel from github, the headers are already included in the source tree. If you don't need all the extra files, it is possible to install only the kernel headers from the Raspberry Pi OS repo.

```
sudo apt install raspberrypi-kernel-headers
```
Note that it can take quite a while for this command to complete, as it installs a lot of small files. There is no progress indicator.

When a new kernel release is made, you will need the headers that match that kernel version. It can take several weeks for the repo to be updated to reflect the latest kernel version. If this happens, the best approach is to clone the kernel as described in the [Build Section](building.md).

