## Memory options in config.txt

### gpu_mem

GPU memory in megabytes. This sets the memory split between the CPU and GPU; the CPU gets the remaining memory. Minimum value is `16`; maximum value is `192`, `448`, or `944`, depending on whether you are using a 256M, 512MB, or 1024MB Pi. The default value is `64`.

Setting `gpu_mem` to low values may automatically disable certain firmware features, as there are some things the GPU cannot do if it has access to too little memory. So if a feature you are trying to use isn't working, try setting a larger GPU memory split.

Using `gpu_mem_256`, `gpu_mem_512`, and `gpu_mem_1024` allows you to swap the same SD card between 256MB, 512MB, and 1024MB Pis without having to edit `config.txt` each time:

### gpu_mem_256

The `gpu_mem_256` command sets the GPU memory in megabytes for the 256MB Raspberry Pi (it is ignored if memory size is not 256MB). This overrides `gpu_mem`. The maximum value is `192` and the default is not set.

### gpu_mem_512

The `gpu_mem_512` command sets the GPU memory in megabytes for the 512MB Raspberry Pi (it is ignored if memory size is not 512MB). This overrides `gpu_mem`. The maximum value is `448` and the default is not set.

### gpu_mem_1024

The `gpu_mem_1024` command sets the GPU memory in megabytes for the 1024MB Raspberry Pi 2 (it is ignored if memory size is not 1024MB). This overrides `gpu_mem`. The maximum value is `944` and the default is not set.

### disable_l2cache

Setting this to `1` disables the CPU's access to the GPU's L2 cache, and requires a corresponding L2 disabled kernel. Default value is `0`.

*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
