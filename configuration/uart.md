# The Raspberry Pi UARTs

The SoCs used on the Raspberry Pis have two built-in UARTs, a [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) and a mini UART. They are implemented using different hardware blocks, so they have slightly different characteristics. However, both are 3.3V devices, which means extra care must be taken when connecting up to an RS232 or other system that utilises different voltage levels. An adapter must be used to convert the voltage levels between the two protocols. Alternatively, 3.3V USB UART adapters can be purchased for very low prices. 
 
By default, on Raspberry Pis equipped with the combined wireless LAN/Bluetooth module, the PL011 UART is connected to the Bluetooth module, while the mini UART is used as the primary UART and will have a Linux console on it. On all other models, the PL011 is used as the primary UART. 

The primary UART is assigned to the Linux console.

The following table summarises the default configuration of the UARTs:

| Model | mini UART | PL011 |
|-------|-----------|-------|
| Raspberry Pi Zero | secondary | primary |
| Raspberry Pi Zero W | primary (disabled) | secondary (Bluetooth) |
| Raspberry Pi 1 | secondary | primary |
| Raspberry Pi 2 | secondary | primary |
| Raspberry Pi 3 | primary (disabled) | secondary (Bluetooth) |
| Raspberry Pi 4 | primary (disabled) | secondary (Bluetooth) |

Linux devices on Raspbian:

| Linux device | Description |
|--------------|-------------|
|`/dev/ttyS0`  |mini UART    |
|`/dev/ttyAMA0`|PL011        |
|`/dev/serial0` |primary UART (Linux console) |
|`/dev/serial1` |secondary UART |

## Mini UART and CPU core frequency

The baud rate of the mini UART is linked to the core frequency of the VPU on the GPU. This means that, as the VPU frequency governor varies the core frequency, the baud rate of the mini UART also changes. This makes the mini UART of limited use in the default state. By default, if the mini UART is selected for use as the primary UART, it will be disabled. To enable it, add `enable_uart=1` to config.txt. This will also fix the core frequency to 250MHz (unless `force_turbo` is set, when it will be fixed to the VPU turbo frequency). When the mini UART is not the primary UART, for example you are using it to connect to the Bluetooth controller, you must add `core_freq=250` to config.txt, otherwise the mini UART will not work.

The default value of the `enable_uart` flag depends on the actual roles of the UARTs, so that if the PL011 is assigned to the Bluetooth module, `enable_uart` defaults to 0. If the mini UART is assigned to the Bluetooth module, then `enable_uart` defaults to 1. Note that if the UARTs are reassigned using a Device Tree Overlay (see below), `enable_uart` defaults will still obey this rule.

## Disable Linux serial console

By default, the primary UART is assigned to the Linux console. If you wish to use the primary UART for other purposes, you must reconfigure Raspbian. This can be done by using [raspi-config](raspi-config.md):

1. Start raspi-config: `sudo raspi-config`.
1. Select option 5 - interfacing options.
1. Select option P6 - serial.
1. At the prompt `Would you like a login shell to be accessible over serial?` answer 'No'
1. At the prompt `Would you like the serial port hardware to be enabled?` answer 'Yes'
1. Exit raspi-config and reboot the Pi for changes to take effect.

## UART output on GPIO pins

By default, the UART transmit and receive pins are on GPIO 14 and GPIO 15 respectively, which are pins 8 and 10 on the GPIO header.

## UARTs and Device Tree

Various UART Device Tree overlay definitions can be found in the kernel GitHub tree. The two most useful overlays are [`disable-bt`](https://github.com/raspberrypi/linux/blob/rpi-4.11.y/arch/arm/boot/dts/overlays/disable-bt-overlay.dts) and [`miniuart-bt`](https://github.com/raspberrypi/linux/blob/rpi-4.11.y/arch/arm/boot/dts/overlays/miniuart-bt-overlay.dts).

`disable-bt` disables the Bluetooth device and restores the PL011 to GPIOs 14 and 15. It is also necessary to disable the system service that initialises the modem, so it doesn't connect to the UART using `sudo systemctl disable hciuart`.

`miniuart-bt` switches the Bluetooth function to use the mini UART (`/dev/ttyS0`), and restores `/dev/ttyAMA0` to GPIOs 14 and 15. Note that this may reduce the maximum usable baudrate (see mini UART limitations below). It is also necessary to edit `/lib/systemd/system/hciuart.service` and replace ttyAMA0 with ttyS0, unless you have a system with udev rules that create /dev/serial0 and /dev/serial1. In this case, use /dev/serial1 instead because it will always be correct. If cmdline.txt uses the alias serial0 to refer to the user-accessible port, the firmware will replace it with the appropriate port whether or not this overlay is used.

There are other UART-specific overlays in the folder. Refer to `/boot/overlays/README` for details on Device Tree overlays, or run `dtoverlay -h overlay-name` for descriptions and usage information.

For full instructions on how to use Device Tree overlays see [this page](device-tree.md). In brief, add a line to the `config.txt` file to enable Device Tree overlays. Note that the `-overlay.dts` part of the filename is removed.
```
...
dtoverlay=disable-bt
...
```
## Relevant differences between PL011 and mini UART

The mini UART has smaller FIFOs. Combined with the lack of flow control, this makes it more prone to losing characters at higher baudrates. It is also generally less capable than the PL011, mainly due to its baud rate link to the VPU clock speed.

The particular deficiencies of the mini UART compared to the PL011 are :
- No break detection
- No framing errors detection
- No parity bit
- No receive timeout interrupt
- No DCD, DSR, DTR or RI signals 

Further documentation on the mini UART can be found in the SoC peripherals document [here](../hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf).
