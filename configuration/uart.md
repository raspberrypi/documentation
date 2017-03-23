# The Raspberry Pi UARTS

The SoC's used on the Raspberry Pi's have two built in UARTS, a [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) and a mini-UART. As they are implemented using different hardware blocks, they have slightly different characteristics. However, both are 3v3 devices, which means extra care must be taken when connecting up to an RS232 or other system that ustilises different voltage levels. An adapter must be used to convert the voltage levels between the two protocols. Alternatively, 3v3 USB UART adapters can be purchased for very low prices. 
 
By default, on Raspberry Pi's equipped with the Wireless/Bluetooth module (Raspberry Pi 3 and Raspberry Pi Zero W), the PL011 UART is connected to the BT module, whilst the mini-UART is used for Linux console output, on all other models the PL011 is used for the Linux console output. 

In Linux device terms, by default, /dev/ttyS0 refers to to the mini-UART, and /dev/ttyAMA0 refers to the PL011. The primary UART is that assigned to the Linux console, which depends on the Raspberry Pi model as described above, and can be accessed via /dev/serial0.

## Mini-UART and CPU Core frequency

The baud rate of the Mini-UART is linked to the core frequency of the VPU on the VC4 GPU. This means that as the VPU frequency governor varies the core frequency, the baud rate of the UART also changes. This makes the UART of limited use in the default state. Also, when the linux console uses the mini-UART (Raspberry Pi 3, ZeroW), this varying baud rate means the console, by default, is disabled. 

The Linux console can be re-enabled by adding the `enable_uart=1` to config.txt. This also fixes the core_freq to 250Mhz (unless force_turbo is set, when it will fixed to 400Mhz) which means the UART baud rate stays consistent. 

The default value of the `enable_uart` flag depends on the actual roles of the UARTS, so that if ttyAMA0 is assigned to the BT module, `enable_uart` defaults to 0, if the mini-UART is assigned to the BT module, then `enable_uart` defaults to 1. Note that if the UARTS are reassigned using a device tree overlay (see below), `enable_uart` defaults will still obey this rule.

## Disabling Linux's use of console UART

In a default install of Raspbian, the primary UART (serial0) is assigned to the Linux console. Using the serial port for other purposes requires this default behaviour to be changed. On startup, `systemd` checks the Linux kernel command line for any console entries and will use the console defined therein. To stop this behaviour the command line needs to have the serial console setting removed.

Edit the kernel command line with `sudo nano /boot/cmdline.txt`. Find the console entry that refers to the serial0 device, and remove it, including the baud rate setting. It will look something like `console=serial0,115200`. Make sure the rest of the line remains the same, as errors in this configuration can stop the Raspberry Pi from booting.

Reboot the Raspberry Pi for the change to take effect.

## UART output on GPIO pins

By default the UART transmit and receive pins are on GPIO 14 and GPIO 15 respectively, which are pins 8 and 10 on the GPIO header.

## UARTs and Device Tree

Various UART device tree overlay definitions can be found in the kernel github tree. The two most useful overlays are [`pi3-disable-bt`](https://github.com/raspberrypi/linux/blob/rpi-4.11.y/arch/arm/boot/dts/overlays/pi3-disable-bt-overlay.dts) and [`pi3-miniuart-bt`](https://github.com/raspberrypi/linux/blob/rpi-4.11.y/arch/arm/boot/dts/overlays/pi3-miniuart-bt-overlay.dts).

`pi3-disable-bt` disables the Bluetooth device and restore UART0/ttyAMA0 to GPIOs 14 & 15. It is also necessary to disable the systemd service that initialises the modem so it doesn't use the UART, `sudo systemctl disable hciuart`.

`pi3-miniuart-bt` switches the Raspberry Pi 3 and Zero W Bluetooth function to use the mini-UART (ttyS0) and restores UART0/ttyAMA0 to GPIOs 14 & 15. Note that this may reduce the maximum usable baudrate (see mini-UART limitations below). It is also necessary to edit /lib/systemd/system/hciuart.service and replace ttyAMA0 with ttyS0, unless you have a system with udev rules that create /dev/serial0 and /dev/serial1, in which case use /dev/serial1 instead because it will always be correct. If cmdline.txt uses the alias serial0 to refer to the user-accessable port then the firmware will replace with the appropriate port whether or not this overlay is used.

There are other UART specific overlays in the folder, refer to the comment section at the top of each overlay for details on its purpose.

For full instructions on how to use device tree overlays see [this page](./device-tree.md), but in brief, add a line to the `config.txt` file to enable device tree overlays. Note that the `-overlay.dts` part of the filename is removed.
```
...
dtoverlay=pi3-disable-bt
...
```
## Relevent differences between PL011 and Mini-UART

The mini-UART has smaller FIFOs, so when combined with the lack of flow control, it is more prone to lose characters at higher baudrates. It is also generally less capable that the PL011, mainly due to its baud rate link to the VPU clock speed.

The particular deficiencies of the mini-UART compared to the PL011 are :
- No Break detection
- No Framing errors detection.
- No Parity bit
- No Receive Time-out interrupt
- No DCD, DSR, DTR or RI signals. 

Furthur documentation on the mini-UART can be found in the SoC peripherals document [here](https://www.raspberrypi.org/wp-content/uploads/2012/02/BCM2835-ARM-Peripherals.pdf)
