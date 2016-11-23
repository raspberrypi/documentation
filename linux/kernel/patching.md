# Patching the kernel

When [building](building.md) your custom kernel you may wish to apply patches, or collections of patches ('patchsets'), to the Linux kernel.

Patchsets are often provided with newer hardware as a temporary measure, before the patches are applied to the upstream Linux kernel ('mainline') and then propagated down to the Raspberry Pi kernel sources. However, patchsets for other purposes exist, for instance to enable a fully pre-emptible kernel for real-time usage.

## Version identification

It's important to check what version of the kernel you have when downloading and applying patches. In a kernel source directory, the following command will show you the version the sources relate to:

```
$ head Makefile -n 3
VERSION = 3
PATCHLEVEL = 10
SUBLEVEL = 25
```

In this instance, the sources are for a 3.10.25 kernel. You can see what version you're running on your system with the `uname -r` command.

## Applying patches

How you apply patches depends on the format in which the patches are made available. Most patches are a single file, and applied with the `patch` utility. For example, let's download and patch our example kernel version with the real-time kernel patches:

```
$ wget https://www.kernel.org/pub/linux/kernel/projects/rt/3.10/older/patch-3.10.25-rt23.patch.gz
$ gunzip patch-3.10.25-rt23.patch.gz
$ cat patch-3.10.25-rt23.patch | patch -p1
```

In our example we simply download the file, uncompress it, and then pass it to the `patch` utility using the `cat` tool and a Unix pipe.

Some patchsets come as mailbox-format patchsets, arranged as a folder of patch files. We can use Git to apply these patches to our kernel, but first we must configure Git to let it know who we are when we make these changes:

```
$ git config --global user.name "Your name"
$ git config --global user.email "your email in here"
```

Once we've done this we can apply the patches:

```
git am -3 /path/to/patches/*
```

If in doubt, consult with the distributor of the patches, who should tell you how to apply them. Some patchsets will require a specific commit to patch against; follow the details provided by the patch distributor.
