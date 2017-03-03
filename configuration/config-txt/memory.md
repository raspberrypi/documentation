## config.txt - Memory Options

### gpu_mem

GPU memory in megabytes. This sets the memory split between the CPU and GPU; the CPU gets the remaining memory. Minimum value is `16`; maximum value is `192`, `448`, or `944`, depending on whether you're using a 256M, 512MB, or 1024MB Pi. The default value is `64`.

Setting `gpu_mem` to low values may automatically disable certain firmware features, as there are some things the GPU simply can't do with too little memory. So if a certain feature you're trying to use isn't working, try setting a larger GPU memory split.

Using `gpu_mem_256`, `gpu_mem_512`, and `gpu_mem_1024` allows you to swap the same SD card between 256MB, 512MB, and 1024MB Pis without having to edit `config.txt` each time:

### gpu_mem_256

GPU memory in megabytes for the 256MB Raspberry Pi (ignored if memory size is not 256MB). This overrides `gpu_mem`. The maximum value is `192` and the default is not set.

### gpu_mem_512

GPU memory in megabytes for the 512MB Raspberry Pi (ignored if memory size is not 512MB). This overrides `gpu_mem`. The maximum value is `448` and the default is not set.

### gpu_mem_1024

GPU memory in megabytes for the 1024MB Raspberry Pi 2 (ignored if memory size is not 1024MB). This overrides `gpu_mem`. The maximum value is `944` and the default is not set.

### disable_l2cache

Setting this to `1` disables the CPU's access to the GPU's L2 cache; requires a corresponding L2 disabled kernel. Default value is `0`.

### disable_pvt

Setting this to `1` disables adjusting the refresh rate of RAM every 500ms; this action measures the RAM's temperature. Default value is `0`.

### CMA - Dynamic memory split

As of 19th November 2012, the firmware and kernel support CMA (Contiguous Memory Allocator), which means the memory split between CPU and GPU is managed dynamically at runtime. However, this is not [officially supported](https://github.com/raspberrypi/linux/issues/503).

You can find an [example config.txt here](http://www.raspberrypi.org/phpBB3/viewtopic.php?p=223549#p223549).

#### cma_lwm

When the GPU has less than `cma_lwm` megabytes of memory available (the low-water mark), it will request some from the CPU.

#### cma_hwm

When the GPU has more than `cma_hwm` megabytes of memory available (the high-water mark), it will release some to the CPU.

The following options need to be in `cmdline.txt` for CMA to work:

```
coherent_pool=6M smsc95xx.turbo_mode=N
```




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
