# Boot options in config.txt 

## start_file, fixup_file

These options specify the firmware files transferred to the VideoCore GPU prior to booting.

`start_file` specifies the VideoCore firmware file to use.
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

## armstub

`armstub` is the filename on the boot partition from which to load the ARM stub. The default ARM stub is stored in firmware and is selected automatically based on the Pi model and various settings.

The stub is a small piece of ARM code that is run before the kernel. Its job is to set up low-level hardware like the interrupt controller before passing control to the kernel.

## arm_peri_high

Set `arm_peri_high` to `1` to enable "High Peripheral" mode on the Pi 4. It is set automatically if a suitable DTB is loaded.

**NOTE**: Enabling "High Peripheral" mode without a compatible device tree will make your system fail to boot. Currently ARM stub support is missing, so you will also need to load a suitable file using `armstub`.

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

## force_eeprom_read

Set this option to `0` to prevent the firmware from trying to read an I2C HAT EEPROM (connected to pins ID_SD & ID_SC) at powerup.

## os_prefix
<a name="os_prefix"></a>

`os_prefix` is an optional setting that allows you to choose between multiple versions of the kernel and Device Tree files installed on the same card. Any value in `os_prefix` is prepended to (stuck in front of) the name of any operating system files loaded by the firmware, where "operating system files" is defined to mean kernels, initramfs, cmdline.txt, .dtbs and overlays. The prefix would commonly be a directory name, but it could also be part of the filename such as "test-". For this reason, directory prefixes must include the trailing `/` character.

In an attempt to reduce the chance of a non-bootable system, the firmware first tests the supplied prefix value for viability - unless the expected kernel and .dtb can be found at the new location/name, the prefix is ignored (set to ""). A special case of this viability test is applied to overlays, which will only be loaded from `${os_prefix}${overlay_prefix}` (where the default value of [`overlay_prefix`](#overlay_prefix) is "overlays/") if `${os_prefix}${overlay_prefix}README` exists, otherwise it ignores `os_prefix` and treats overlays as shared.

(The reason the firmware checks for the existence of key files rather than directories when checking prefixes is twofold - the prefix may not be a directory, and not all boot methods support testing for the existence of a directory.)

N.B. Any user-specified OS file can bypass all prefixes by using an absolute path (with respect to the boot partition) - just start the file path with a `/`, e.g. `kernel=/my_common_kernel.img`.

See also [`overlay_prefix`](#overlay_prefix) and [`upstream_kernel`](#upstream_kernel).

## overlay_prefix
<a name="overlay_prefix"></a>

Specifies a subdirectory/prefix from which to load overlays - defaults to `overlays/` (note the trailing `/`). If used in conjunction with [`os_prefix`](#os_prefix), the `os_prefix` comes before the `overlay_prefix`, i.e. `dtoverlay=disable-bt` will attempt to load `${os_prefix}${overlay_prefix}disable-bt.dtbo`.

Note that unless `${os_prefix}${overlay_prefix}README` exists, overlays are shared with the main OS (i.e. `os_prefix` is ignored).

## uart_2ndstage

Setting `uart_2ndstage=1` causes the second-stage loader (`bootcode.bin` on devices prior to the Raspberry Pi 4, or the boot code in the  EEPROM for Raspberry Pi 4 devices) and the main firmware (`start*.elf`) to output diagnostic information to UART0. 

Be aware that output is likely to interfere with Bluetooth operation unless it is disabled (`dtoverlay=disable-bt`) or switched to the other UART (`dtoverlay=miniuart-bt`), and if the UART is accessed simultaneously to output from Linux then data loss can occur leading to corrupted output. This feature should only be required when trying to diagnose an early boot loading problem.

## upstream_kernel
<a name="upstream_kernel"></a>

If `upstream_kernel=1` is used, the firmware sets [`os_prefix`](#os_prefix) to "upstream/", unless it has been explicitly set to something else, but like other `os_prefix` values it will be ignored if the required kernel and .dtb file can't be found when using the prefix.

The firmware will also prefer upstream Linux names for DTBs (`bcm2837-rpi-3-b.dtb` instead of `bcm2710-rpi-3-b.dtb`, for example). If the upstream file isn't found the firmware will load the downstream variant instead  and automatically apply the "upstream" overlay to make some adjustments. Note that this process happens _after_ the `os_prefix` has been finalised.

*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
