# The Kernel Command Line

The Linux kernel accepts a command line of parameters during boot. On the Raspberry Pi, this command line is defined in a file in the boot partition, called cmdline.txt. This is a simple text file that can be edited using any text editor, e.g. Nano.
```
sudo nano /boot/cmdline.txt
```
Note that we have to use `sudo` to edit anything in the boot partition.

## Command Line Options

There are many kernel command line parameters, some of which are defined by the kernel. Others are defined by code that the kernel may be using, such as the Plymouth splash screen system.

#### Standard Entries

 - console: defines the serial console. There are usually two entries:
     - `console=serial0,115200`
     - `console=tty1`
 - root: defines the location of the root filesystem, e.g. `root=/dev/mmcblk0p2` means multmedia card block 0 partition 2.
 - rootfstype: defines what type of filesystem the rootfs uses, e.g. `rootfstype=ext4`
 - elevator: specifies the I/O scheduler to use. `elevator=deadline` means the kernel imposes a deadline on all I/O operations to prevent request starvation.
 - quiet: sets the default kernel log level to `KERN_WARNING`, which supresses all but very serious log messages during boot.


#### Other Entries (not exhaustive)

 - splash: tells the boot to use a splash screen via the Plymouth module.
 - plymouth.ignore_serial_console
 - dwc_otg.lpm_enable: turns off LPM in the dwc_otg (On The Go) driver.
 - dwc_otg.speed: sets the speed of the USB property. `dwc_otg.speed=1` will set it to USBv1.0 speed.
 - smsc95xx.turbo_mode: enables/disables the wired networking driver turbo mode. `smsc95xx.turbo_mode=N` turns turbo mode off.
 - usbhid.mousepoll: specifies the mouse polling interval. If you have problems with a slow or erratic wireless mouse, setting this to 0 might help: `usbhid.mousepoll=0`.

