# Memory options in config.txt

## gpu_mem

Specifies how much memory, in megabytes, to reserve for the exclusive use of the GPU: the remaining memory is allocated to the ARM CPU. The default value is `76`, except on the Pi Zero and Pi 1 where it is `64`. You should set `gpu_mem` to the lowest possible value to ensure best performance. If a particular graphics feature is not working correctly, try increasing the value of `gpu_mem`, being mindful of the recommended maximums shown below.

The recommended maximum values are as follows:

| total RAM | `gpu_mem` recommended maximum |
|-----------|-------------------------------|
| 256MB     | `128`                         |
| 512MB     | `384`                         |
| 1GB or greater | `512`                    |

 It is possible to set `gpu_mem` to larger values, however this should be avoided since it can cause problems, such as preventing Linux from booting. There is no performance advantage to specifying values larger than is necessary. The minimum value is `16`, however this disables certain GPU features.

On the Raspberry Pi 4 the 3D component of the GPU has its own memory management unit (MMU), and does not use memory from the `gpu_mem` allocation. Instead memory is allocated dynamically within Linux. This may allow a smaller value to be specified for `gpu_mem` on the Pi 4, compared to previous models.

You can also use `gpu_mem_256`, `gpu_mem_512`, and `gpu_mem_1024` to allow swapping the same SD card between Pis with different amounts of RAM without having to edit `config.txt` each time:

## gpu_mem_256

The `gpu_mem_256` command sets the GPU memory in megabytes for Raspberry Pis with 256MB of memory. (It is ignored if memory size is not 256MB). This overrides `gpu_mem`.

## gpu_mem_512

The `gpu_mem_512` command sets the GPU memory in megabytes for Raspberry Pis with 512MB of memory. (It is ignored if memory size is not 512MB). This overrides `gpu_mem`.

## gpu_mem_1024

The `gpu_mem_1024` command sets the GPU memory in megabytes for Raspberry Pis with 1GB or more of memory. (It is ignored if memory size is smaller than 1GB). This overrides `gpu_mem`.

## disable_l2cache

Setting this to `1` disables the CPU's access to the GPU's L2 cache and requires a corresponding L2 disabled kernel. Default value on BCM2835 is `0`. On BCM2836, BCM2837, and BCM2711, the ARMs have their own L2 cache and therefore the default is `1`. The standard Pi kernel.img and kernel7.img builds reflect this difference in cache setting.

*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
