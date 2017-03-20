# The Raspberry Pi UARTS

The SoC's used on the Raspberry Pi's have two built in UARTS, a [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) and a mini-UART. As they are implemented using different hardware blocks, they have slightly different characteristics. However, both are 3v3 devices, which means extra care must be taken when connecting up to an RS232 or other system that ustilises different voltage levels. An adapter must be used to convert the voltage levels between the two protocols. Alternatively, 3v3 USB UART adapters can be purchased for very low prices. 
 
By default, on Raspberry Pi's equipped with the Wireless/Bluetooth module (Raspberry Pi 3 and Raspberry Pi Zero W), the PL011 UART is connected to the BT/Wireless module, whilst the mini-UART is used for Linux console output, on all other models the PL011 is used for the Linux console output. 

In Linux device terms, by default, /dev/ttyS0 refers to to the mini-UART, and /dev/ttyAMA0 refers to the PL011. The primary UART is that assigned to the Linux console, which depends on the Raspberry Pi model as described above, and can be accessed via /dev/serial0.

## Mini-UART and CPU Core frequency

The baud rate of the Mini-UART is linked to the core frequency of the VPU on the VC4 GPU. This means that as the VPU frequency governor varies the core frequency, the baud rate of the UART also changes. This makes the UART of limited use in the default state. Also, when the linux console uses the mini-UART (Raspberry Pi 3, ZeroW), by default this is disabled for this very reason. 

The Linux console can be re-enabled by adding the `enable_uart=1` to config.txt. This also fixes the core_freq to 250Mhz (unless force_turbo is set, when it will fixed to 400Mhz) which means the UART baud rate stays consistent. By default, `enable_uart=1` on Raspberry Pi's without the Wireless/BT module, and `enable_uart=0` on those with.

### UART output on GPIO pins

By default the UART transmit and receive pins are on GPIO 14 and GPIO 15 respectively, which are pins 8 and 10 on the GPIO header.


### UARTs and Device Tree

Various UART device tree overlay definitions can be found in the kernel github tree.

This link is to an overlay that switches the Pi3 Bluetooth function to use the mini-UART (ttyS0) and restores UART0/ttyAMA0 over GPIOs 14 & 15.

https://github.com/raspberrypi/linux/blob/rpi-4.11.y/arch/arm/boot/dts/overlays/pi3-miniuart-bt-overlay.dts

There are other UART specific overlays in the folder, refer to the comment section at the top of each overlay for details on its purpose.


### Relevent differences between PL011 and Mini-UART

The mini-UART has smaller FIFOs, so when combined with the lack of flow control, it is more prone to lose characters at higher baudrates. It is also generally less capable that the PL011, mainly due to its baud rate link to the VPU clock speed.
