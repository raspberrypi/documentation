## Boot options in config.txt 

### start_file, fixup_file

These options specify the firmware files transfered to the Videocore GPU prior to boot.

`start_file` specifies the Videocore (VC4) firmware file to use.
`fixup_file` specifies the file used to fixup memory locations used in the `start_file` to match the GPU memory split. Note the the `start_file` and the `fixup_file` are linked - you cannot mix them.

### start_x, start_debug

These provide a shortcut to some alternative `start_file` and `fixup_file` settings.

`start_x=1` implies
   `start_file=start_x.elf`
   `fixup_file=fixup_x.dat`
   
`start_debug=1` implies
   `start_file=start_db.elf`
   `fixup_file=fixup_db.dat`

`start_x=1` should be specified when using the camera module. Enabling the camera via `raspi-config` will set this automatically.

### disable_commandline_tags

Set the `disable_commandline_tags` command to `1` to stop `start.elf` from filling in ATAGS (memory from `0x100`) before launching the kernel.

### cmdline

`cmdline` is the alternative filename on the boot partition from which to read the kernel command line string; the default value is `cmdline.txt`.

### kernel

`kernel` is the alternative filename on the boot partition to use when loading the kernel. The default value is `kernel.img`.

### kernel_address

`kernel_address` is the memory address into which the kernel image should be loaded. 32-bit kernels are loaded to address `0x8000` by default, and 64-bit kernels to address `0x80000`. If `kernel_old` is set, kernels are loaded to the address `0x0`.

### kernel_old

Set `kernel_old` to `1` to load the kernel at the memory address `0x0`.

### ramfsfile

`ramfsfile` is the optional filename on the boot partition of a ramfs to load. More information is available [here](https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=10532).

### ramfsaddr

`ramfsaddr` is the memory address into which the `ramfsfile` should be loaded.

### initramfs

The `initramfs` command specifies both the ramfs filename **and** the memory address at which to load it. It performs the actions of both `ramfsfile` and `ramfsaddr` in one parameter. Example values are: `initramfs initramf.gz 0x00800000`. **NOTE:** This option uses different syntax from all the other options, and you should not use a `=` character here.

### init_uart_baud

`init_uart_baud` is the initial UART baud rate. The default value is `115200`.

### init_uart_clock

`init_uart_clock` is the initial UART clock frequency. The default value is `3000000` (3MHz).

### bootcode_delay

The `bootcode_delay` command means wait for a given number of seconds in `bootcode.bin` before loading `start.elf`: the default value is `0`.

This is particularly useful to insert a delay before reading the EDID of the monitor. This is useful if the Pi and monitor are powered from the same source, but the monitor takes longer to start up than the Pi. Try setting this value if the display detection is wrong on initial boot, but is correct if you soft-reboot the Pi without removing power from the monitor.

### boot_delay

The `boot_delay` command means wait for a given number of seconds in `start.elf` before loading the kernel: the default value is `1`. The total delay in milliseconds is calculated as `(1000 x boot_delay) + boot_delay_ms`. This can be useful if your SD card needs a while to get ready before Linux is able to boot from it.

### boot_delay_ms

The `boot_delay_ms` command means wait for a given number of milliseconds in `start.elf`, together with `boot_delay`, before loading the kernel. The default value is `0`.

### disable_splash

If `disable_splash` is set to `1`, the rainbow splash screen will not be shown on boot. The default value is `0`.





*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
