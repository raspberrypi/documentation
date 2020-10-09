# The Kernel Command Line

The Linux kernel accepts a command line of parameters during boot. On the Raspberry Pi, this command line is defined in a file in the boot partition, called cmdline.txt. This is a simple text file that can be edited using any text editor, e.g. Nano.
```
sudo nano /boot/cmdline.txt
```
Note that we have to use `sudo` to edit anything in the boot partition, and that all parameters in `cmdline.txt` must be on the same line (no carriage returns).

The command line that was passed to the kernel at boot time can be displayed using `cat /proc/cmdline`. It will not be exactly the same as that in `cmdline.txt` as the firmware can make changes to it prior to launching the kernel.

## Command Line Options

There are many kernel command line parameters, some of which are defined by the kernel. Others are defined by code that the kernel may be using, such as the Plymouth splash screen system.

#### Standard Entries

 - console: defines the serial console. There are usually two entries:
     - `console=serial0,115200`
     - `console=tty1`
 - root: defines the location of the root filesystem, e.g. `root=/dev/mmcblk0p2` means multimedia card block 0 partition 2.
 - rootfstype: defines what type of filesystem the rootfs uses, e.g. `rootfstype=ext4`
 - elevator: specifies the I/O scheduler to use. `elevator=deadline` means the kernel imposes a deadline on all I/O operations to prevent request starvation.
 - quiet: sets the default kernel log level to `KERN_WARNING`, which suppresses all but very serious log messages during boot.

#### Display Entries in FKMS and KMS modes

The firmware automatically adds a preferred resolution and overscan settings via an entry such as:

```video=HDMI-A-1:1920x1080M@60,margin_left=0,margin_right=0,margin_top=0,margin_bottom=0```

This default entry can be modified by duplicating the entry above manually in /boot/cmdline.txt and making required changes to the margin parameters. In addition, it is possible to add rotation and reflect parameters as documented in the standard [Linux framebuffer documentation](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/Documentation/fb/modedb.rst). By default the `margin_*` options are set from the `overscan` entries in config.txt, if present. The firmware can be prevented from making any KMS specific changes to the command line by adding `disable_fw_kms_setup=1` to `config.txt`

An example entry may be as follows:

```video=HDMI-A-1:1920x1080M@60,margin_left=0,margin_right=0,margin_top=0,margin_bottom=0,rotate=90,reflect_x```

Possible options for the display type, the first part of the `video=` entry,  are as follows:

| video option  | Display |
|:---:|:---|
| HDMI-A-1      | HDMI 1 (HDMI 0 on silkscreen of Pi4B, HDMI on single HDMI boards) |
| HDMI-A-2      | HDMI 2 (HDMI 1 on silkscreen of Pi4B) |
| DSI-1         | DSI or DPI |
| Composite-1   | Composite  |

#### Other Entries (not exhaustive)

 - splash: tells the boot to use a splash screen via the Plymouth module.
 - plymouth.ignore-serial-consoles: normally if the Plymouth module is enabled it will prevent boot messages from appearing on any serial console which may be present. This flag tells Plymouth to ignore all serial consoles, making boot messages visible again, as they would be if Plymouth was not running.
 - dwc_otg.lpm_enable: turns off Link Power Management (LPM) in the dwc_otg driver; the dwc_otg driver is the driver for the USB controller built into the Raspberry Pi.
 - dwc_otg.speed: sets the speed of the USB controller. `dwc_otg.speed=1` will set it to full speed (USB 1.0), which is slower than high speed (USB 2.0). This option should not be set except during troubleshooting of problems with USB devices.
 - smsc95xx.turbo_mode: enables/disables the wired networking driver turbo mode. `smsc95xx.turbo_mode=N` turns turbo mode off.
 - usbhid.mousepoll: specifies the mouse polling interval. If you have problems with a slow or erratic wireless mouse, setting this to 0 might help: `usbhid.mousepoll=0`.

