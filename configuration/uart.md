# UART configuration

There are two types of UART available on the Raspberry Pi -  [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) and mini UART. The PL011 is a capable, broadly 16550-compatible UART, while the mini UART has a reduced feature set.

All UARTs on the Raspberry Pi are 3.3V only - damage will occur if they are connected to 5V systems. An adaptor can be used to connect to 5V systems. Alternatively, low-cost USB to 3.3V serial adaptors are available from various third parties.

## Pi Zero, 1, 2 and 3 - two UARTs

The Raspberry Pi Zero, 1, 2, and 3 each contain two UARTs as follows:

| Name | Type |
|------|------|
|UART0 |PL011 |
|UART1 |mini UART |

## Pi 4 - six UARTS

The Raspberry Pi 4 has four additional PL011s, which are disabled by default. The full list of UARTs on the Pi 4 is:

| Name | Type |
|------|------|
|UART0 |PL011 |
|UART1 |mini UART |
|UART2 |PL011 |
|UART3 |PL011 |
|UART4 |PL011 |
|UART5 |PL011 |

## Primary UART

On the Raspberry Pi, one UART is selected to be present on GPIO 14 (transmit) and 15 (receive) - this is the primary UART. By default, this will also be the UART on which a Linux console may be present. Note that GPIO 14 is pin 8 on the GPIO header, while GPIO 15 is pin 10.

## Secondary UART

The secondary UART is not normally present on the GPIO connector. By default, the secondary UART is connected to the Bluetooth side of the combined wireless LAN/Bluetooth controller, on models which contain this controller.

## Configuration

By default, only UART0 is enabled. The following table summarises the assignment of the first two UARTs:

| Model | first PL011 (UART0)| mini UART |
|-------|-----------|-------|
| Raspberry Pi Zero |  primary | secondary |
| Raspberry Pi Zero W | secondary (Bluetooth) | primary |
| Raspberry Pi 1 | primary | secondary |
| Raspberry Pi 2 | primary | secondary |
| Raspberry Pi 3 | secondary (Bluetooth) | primary |
| Raspberry Pi 4 | secondary (Bluetooth) | primary |

Note: the mini UART is disabled by default, whether it is designated primary or secondary UART.

Linux devices on Raspberry Pi OS:

| Linux device | Description |
|--------------|-------------|
|`/dev/ttyS0`  |mini UART    |
|`/dev/ttyAMA0`|first PL011 (UART0) |
|`/dev/serial0` |primary UART |
|`/dev/serial1` |secondary UART |

Note: `/dev/serial0` and `/dev/serial1` are symbolic links which point to either `/dev/ttyS0` or `/dev/ttyAMA0`.

## Mini UART and CPU core frequency

In order to use the mini UART, you need to configure the Raspberry Pi to use a fixed VPU core clock frequency. This is because the mini UART clock is linked to the VPU core clock, so that when the core clock frequency changes, the UART baud rate will also change. The `enable_uart` and `core_freq` settings can be added to `config.txt` to change the behaviour of the mini UART. The following table summarises the possible combinations:

| Mini UART set to | core clock | Result |
|------------------|------------|--------|
| primary UART     | variable   | mini UART disabled |
| primary UART     | fixed by setting `enable_uart=1` | mini UART enabled, core clock fixed to 250MHz, or if `force_turbo=1` is set, the VPU turbo frequency |
| secondary UART   | variable   | mini UART disabled |
| secondary UART   | fixed by setting `core_freq=250` | mini UART enabled |

The default state of the `enable_uart` flag depends on which UART is the primary UART:

| Primary UART | Default state of enable_uart flag |
|--------------|-----------------------------------|
| mini UART    | 0 |
| first PL011 (UART0)       | 1 |

## Disable Linux serial console

By default, the primary UART is assigned to the Linux console. If you wish to use the primary UART for other purposes, you must reconfigure Raspberry Pi OS. This can be done by using [raspi-config](raspi-config.md):

1. Start raspi-config: `sudo raspi-config`.
1. Select option 3 - Interface Options.
1. Select option P6 - Serial Port.
1. At the prompt `Would you like a login shell to be accessible over serial?` answer 'No'
1. At the prompt `Would you like the serial port hardware to be enabled?` answer 'Yes'
1. Exit raspi-config and reboot the Pi for changes to take effect.

## Enabling early console (earlycon) for Linux

Although the Linux kernel starts the UARTs relatively early in the boot process, it is still long after some critical bits of infrastructure have been set up. A failure in those early stages can be hard to diagnose without access to the kernel log messages from that time. That's the problem that the "earlycon" mechanism was created to work around. Consoles that support earlycon usage present an additional interface to the kernel that allows for simple, synchronous output - printk won't return until the characters have been output to the UART.

Enable earlycon with a kernel command line parameter - add one of the following to `cmdline.txt`, depending on which UART is the primary:
```
# For Pi 4 and Compute Module 4 (BCM2711)
earlycon=uart8250,mmio32,0xfe215040
earlycon=pl011,mmio32,0xfe201000

# For Pi 2, Pi 3 and Compute Module 3 (BCM2836 & BCM2837)
earlycon=uart8250,mmio32,0x3f215040
earlycon=pl011,mmio32,0x3f201000

# For Pi 1, Pi Zero and Compute Module (BCM2835)
earlycon=uart8250,mmio32,0x20215040
earlycon=pl011,mmio32,0x20201000
```
The baudrate is set to 115200.

N.B. Selecting the wrong early console can prevent the Pi from booting.

## UARTs and Device Tree

Various UART Device Tree overlay definitions can be found in the [kernel GitHub tree](https://github.com/raspberrypi/linux). The two most useful overlays are [`disable-bt`](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/arch/arm/boot/dts/overlays/disable-bt-overlay.dts) and [`miniuart-bt`](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/arch/arm/boot/dts/overlays/miniuart-bt-overlay.dts).

`disable-bt` disables the Bluetooth device and makes the first PL011 (UART0) the primary UART. You must also disable the system service that initialises the modem, so it does not connect to the UART, using `sudo systemctl disable hciuart`.

`miniuart-bt` switches the Bluetooth function to use the mini UART, and makes the first PL011 (UART0) the primary UART. Note that this may reduce the maximum usable baud rate (see mini UART limitations below). You must also set the VPU core clock to a fixed frequency using either `force_turbo=1` or `core_freq=250`.

The overlays `uart2`, `uart3`, `uart4`, and `uart5` are used to enable the four additional UARTs on the Pi 4. There are other UART-specific overlays in the folder. Refer to `/boot/overlays/README` for details on Device Tree overlays, or run `dtoverlay -h overlay-name` for descriptions and usage information.

For full instructions on how to use Device Tree overlays see [this page](device-tree.md). In brief, add a line to the `config.txt` file to apply a Device Tree overlay. Note that the `-overlay.dts` part of the filename is removed. For example:
```
dtoverlay=disable-bt
```

## Relevant differences between PL011 and mini UART

The mini UART has smaller FIFOs. Combined with the lack of flow control, this makes it more prone to losing characters at higher baudrates. It is also generally less capable than a PL011, mainly due to its baud rate link to the VPU clock speed.

The particular deficiencies of the mini UART compared to a PL011 are :
- No break detection
- No framing errors detection
- No parity bit
- No receive timeout interrupt
- No DCD, DSR, DTR or RI signals 

Further documentation on the mini UART can be found in the SoC peripherals document [here](../hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf).
