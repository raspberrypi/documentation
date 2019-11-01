# Memory options in config.txt

## gpu_mem

GPU memory in megabytes, sets the memory split between the CPU and GPU; the CPU gets the remaining memory. The minimum value is `16`; the technical maximum value is `192`, `448`, or `944`, depending on whether you are using a 256MB, 512MB, or 1024MB Pi. The default value is `64`, values above `512` will not provide increased performance and should not be used. For the Raspberry Pi 4, which is available in 1GB, 2GB and 4GB versions, the minimum and maximum values are the same as for a 1GB device.

`gpu_mem` refers to memory that is addressable from the GPU, which includes the VPU, HVS, legacy codecs (e.g. H264), and camera, and on devices before the Raspberry Pi 4, the 3D system. The Raspberry Pi 4 3D system has it's own Memory Mangement Unit (MMU) so textures and other GL resources are not allocated from the `gpu_mem` but Linux system memory instead. This means that `gpu_mem` can be set to a lower value, so even if you are using the H264 and camera then 128MB will probably be enough. On earlier models without the 3D MMU, you may need up to 256 or 512 in some more unusual cases. 

For performance reasons, you should set `gpu_mem` as low as possible to give the Linux system as much memory as possible. However, setting `gpu_mem` to too low values may automatically disable certain firmware features, as there are some things the GPU cannot do if it has access to too little memory. So if a feature you are trying to use isn't working, try setting a larger GPU memory split.

Values of `gpu_mem` over 512 are not recommended, will provide no performance improvements, and are untested.

Using `gpu_mem_256`, `gpu_mem_512`, and `gpu_mem_1024` allows you to swap the same SD card between 256MB, 512MB, and 1024MB Pis without having to edit `config.txt` each time:

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
