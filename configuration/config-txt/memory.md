# Memory options in config.txt

## gpu_mem

Specifies how much memory, in megabytes, to reserve for the exclusive use of the GPU: the remaining memory is allocated to the ARM CPU. The default value is `64`. The recommended maximum values are as follows:

| total RAM | `gpu_mem` recommended maximum |
---------------------------------------------
| 256MB     | `128`                         |
| 512MB     | `384`                         |
| 1GB or greater | `512`                    |

The minimum value of `gpu_mem` is `16`, however this disables certain GPU features. You should set `gpu_mem` to the lowest possible value for best performance. If a particular graphics feature is not working correctly, try increasing the value of `gpu_mem`, being mindful of the recommendations in the above table. It is possible to set `gpu_mem` to larger values, however this can cause problems for the operating system so should generally be avoided.

On the Raspberry Pi 4 the 3D component of the GPU has its own memory management unit (MMU), and does not use memory from the `gpu_mem` allocation. Instead memory is allocated dynamically by the operating system.

You can also use `gpu_mem_256`, `gpu_mem_512`, and `gpu_mem_1024` to allow swapping the same SD card between Pis with different amounts of RAM without having to edit `config.txt` each time:

## gpu_mem_256

The `gpu_mem_256` command sets the GPU memory in megabytes for the 256MB Raspberry Pi. (It is ignored if memory size is not 256MB). This overrides `gpu_mem`. The maximum value is `192`, and the default is not set.

## gpu_mem_512

The `gpu_mem_512` command sets the GPU memory in megabytes for the 512MB Raspberry Pi. (It is ignored if memory size is not 512MB). This overrides `gpu_mem`. The maximum value is `448`, and the default is not set.

## gpu_mem_1024

The `gpu_mem_1024` command sets the GPU memory in megabytes for Raspberry Pi devices with 1024MB or more of memory. (It is ignored if memory size is smaller than 1024MB). This overrides `gpu_mem`. The maximum value is `944`, and the default is not set.

## disable_l2cache

Setting this to `1` disables the CPU's access to the GPU's L2 cache and requires a corresponding L2 disabled kernel. Default value on BCM2835 is `0`. On BCM2836, BCM2837, and BCM2711, the ARMs have their own L2 cache and therefore the default is `1`.
The standard Pi kernel.img and kernel7.img builds reflect this difference in cache setting.

*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
