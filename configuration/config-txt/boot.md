# Boot options in config.txt 

## start_file, fixup_file

These options specify the firmware files transferred to the Videocore GPU prior to booting.

`start_file` specifies the Videocore (VC4) firmware file to use.
`fixup_file` specifies the file used to fix up memory locations used in the `start_file` to match the GPU memory split. Note that the `start_file` and the `fixup_file` are a matched pair - using unmatched files will stop the board from booting. This is an advanced option, so we advise that you use `start_x` and `start_debug` rather than this option.

## start_x, start_debug

These provide a shortcut to some alternative `start_file` and `fixup_file` settings, and are the recommended methods for selecting firmware configurations.

`start_x=1` implies
   `start_file=start_x.elf`
   `fixup_file=fixup_x.dat`
   
 On the Pi 4, if the files `start4x.elf` and `fixup4x.dat` are present, these files will be used instead.
   
`start_debug=1` implies
   `start_file=start_db.elf`
   `fixup_file=fixup_db.dat`

There is no specific handling for the Pi 4, so if you wish to use the Pi 4 debug firmware files, you need to manually specify `start_file` and `fixup_file`.

`start_x=1` should be specified when using the camera module. Enabling the camera via `raspi-config` will set this automatically.

## disable_commandline_tags

Set the `disable_commandline_tags` command to `1` to stop `start.elf` from filling in ATAGS (memory from `0x100`) before launching the kernel.

## cmdline

`cmdline` is the alternative filename on the boot partition from which to read the kernel command line string; the default value is `cmdline.txt`.

## kernel

`kernel` is the alternative filename on the boot partition to use when loading the kernel. The default value on the Pi 1, Pi Zero, and Compute Module is `kernel.img`, and on the Pi 2, Pi 3, and Compute Module 3 it is `kernel7.img`. On the Pi4, it is `kernel7l.img`. 

## arm_64bit

If set to non-zero, forces the kernel loading system to assume a 64-bit kernel, starts the processors up in 64-bit mode, and sets `kernel8.img` to be the kernel image loaded, unless there is an explicit `kernel` option defined in which case that is used instead. Defaults to 0 on all platforms. **NOTE**: 64-bit kernels must be uncompressed image files.

Note that the 64-bit kernel will only work on the Pi4, Pi3, and Pi2B rev1.2 boards with latest firmware.

## arm_control

**DEPRECATED - use arm_64bit to enable 64-bit kernels**.

Sets board-specific control bits.

## kernel_address

`kernel_address` is the memory address to which the kernel image should be loaded. 32-bit kernels are loaded to address `0x8000` by default, and 64-bit kernels to address `0x80000`. If `kernel_old` is set, kernels are loaded to the address `0x0`.

## kernel_old

Set `kernel_old` to `1` to load the kernel to the memory address `0x0`.

## ramfsfile

`ramfsfile` is the optional filename on the boot partition of a ramfs to load. N.B. Sufficiently new firmware supports the loading of multiple ramfs files - separate the multiple file names with commas, taking care not to exceed the 80-character line length limit. All the loaded files are concatenated in memory and treated as a single ramfs blob. More information is available [here](https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=10532).

## ramfsaddr

`ramfsaddr` is the memory address to which the `ramfsfile` should be loaded.

## initramfs

The `initramfs` command specifies both the ramfs filename **and** the memory address to which to load it. It performs the actions of both `ramfsfile` and `ramfsaddr` in one parameter. The address can also be `followkernel` (or `0`) to place it in memory after the kernel image. Example values are: `initramfs initramf.gz 0x00800000` or `initramfs init.gz followkernel`. As with `ramfsfile`, newer firmwares allow the loading of multiple files by comma-separating their names. **NOTE:** This option uses different syntax from all the other options, and you should not use a `=` character here.

## init_uart_baud

`init_uart_baud` is the initial UART baud rate. The default value is `115200`.

## init_uart_clock

`init_uart_clock` is the initial UART clock frequency. The default value is `48000000` (48MHz). Note that this clock only applies to UART0 (ttyAMA0 in Linux), and that the maximum baudrate for the UART is limited to 1/16th of the clock. The default UART on the Pi 3 and Pi Zero is UART1 (ttyS0 in Linux), and its clock is the core VPU clock - at least 250MHz.

## bootcode_delay

The `bootcode_delay` command delays for a given number of seconds in `bootcode.bin` before loading `start.elf`: the default value is `0`.

This is particularly useful to insert a delay before reading the EDID of the monitor, for example if the Pi and monitor are powered from the same source, but the monitor takes longer to start up than the Pi. Try setting this value if the display detection is wrong on initial boot, but is correct if you soft-reboot the Pi without removing power from the monitor.

## boot_delay

The `boot_delay` command instructs to wait for a given number of seconds in `start.elf` before loading the kernel: the default value is `1`. The total delay in milliseconds is calculated as `(1000 x boot_delay) + boot_delay_ms`. This can be useful if your SD card needs a while to get ready before Linux is able to boot from it.

## boot_delay_ms

The `boot_delay_ms` command means wait for a given number of milliseconds in `start.elf`, together with `boot_delay`, before loading the kernel. The default value is `0`.

## disable_splash

If `disable_splash` is set to `1`, the rainbow splash screen will not be shown on boot. The default value is `0`.

## enable_gic (Pi 4B only)

On the Raspberry Pi 4B, if this value is set to `0` then the interrupts will be routed to the ARM cores using the legacy interrupt controller, rather than via the GIC-400. The default value is `1`.



*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
