# The Raspberry Pi UARTS

The SoC's used on the Raspberry Pi's have two built in UARTS, a [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) and a mini-UART. As they are implemented using different hardware blocks, they have slightly different characteristics. However, both are 3v3 devices, which means extra care must be taken when connecting up to an RS232 system. An adapter must be used to convert the voltage levels between the two protocols. Alternatively, 3v3 USB UART adapters can be purchased for very low prices. 
 
By default, on Raspberry Pi's equipped with the Wireless/Bluetooth module (Raspberry Pi 3 and Raspberry Pi Zero W), the PL011 UART is connected to the BT/Wireless module, whilst the mini-UART is used for Linux console output, on all other models the PL011 is used for the Linux console output. 

In Linux device terms, by default, /dev/ttyS0 refers to to the mini-UART, and /dev/ttyAMA0 refers to the PL011.

## Mini-UART and CPU Core frequency

The baud rate of the Mini-UART is linked to the core frequency of the CPU. This means that as the CPU frequency governor varies the core frequency, the baud rate of the UART also changes. This makes the UART of limited use in the default state. Also, when the linux console uses the mini-UART, by default this is disabled for the same reason. 

The Linux console can be re-enabled by adding the `enable_uart=1` to config.txt. This also fixes the core_freq to 250 which means the UART baud rate stays consistent. By default, `enable_uart=1` on Raspberry Pi's without the Wireless/BT module, and `enable_uart=0` on those with.



### UART output on GPIO pins

By default the UART transmit and receive pins are on GPIO 14 and GPIO 15 respectively, which are pins 8 and 10 on the GPIO header.


### UARTs and Device Tree

The UART device tree definitions can be found in the kernel github tree.

### Relevent differences between PL011 and Mini-UART

The mini-UART has smaller FIFOs, so when combined with the lack of flow control, it is more prone to lose characters at higher baudrates.
