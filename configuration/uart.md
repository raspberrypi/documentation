# UART configuration

## Hardware

All Raspberry Pi computers have at least two UARTs. The Raspberry Pi 4 family (BCM2711) has six UARTs.

There are two different types of UART devices available on the Raspberry Pi:
* [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html), patterned on the [16550 UART](https://en.wikipedia.org/wiki/16550_UART) chip.
* mini UART, patterned on the [8250 UART](https://en.wikipedia.org/wiki/8250_UART) chip.

The naming and numbering of the UARTs can be confusing because they use different names and numbers in different contexts. These names from Broadcom are authoritative:

| SoC | UART0 | UART1 | UART2 | UART3 | UART4 | UART5 |
| --- | --- | --- | --- | --- | --- | --- |
| BCM2835 | PL011 | mini UART |
| BCM2836 | PL011 | mini UART |
| BCM2837 | PL011 | mini UART |
| BCM2711 | PL011 | mini UART | PL011 | PL011 | PL011 | PL011 |

Inside the Raspberry Pi, the UARTs are able to connect in several ways. UART0 and UART1 can connect to either the GPIO lines, or the onboard Bluetooth module, if there is one. UARTs two through five connect to the GPIO lines and nowhere else.

See the [Raspberry Pi 4 Model B Datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711/rpi_DATA_2711_1p0_preliminary.pdf) section _5.1.2 GPIO Alternate Functions_, for pinout details. Earlier models are similar but with only the first two UARTs.

### Voltages

All the onboard Raspberry Pi UARTs are 3.3V ([CMOS](https://en.wikipedia.org/wiki/CMOS) [logic level](https://en.wikipedia.org/wiki/Logic_level)). Do not connect Raspberry Pi UARTs to 5V ([TTL logic level](https://en.wikipedia.org/wiki/Transistor%E2%80%93transistor_logic)) circuits, because the Raspberry Pi will be damaged. [Level shifters](https://en.wikipedia.org/wiki/Level_shifter) are inexpensive and readily available.

## Software support

Raspberry Pi OS ships with drivers for the onboard UARTs.

PL011s appear as [character devices](https://en.wikipedia.org/wiki/Device_file#Character_devices) `/dev/ttyAMA*`. If there are multiple PL011s, they're in the same _order_ as the Broadcom documentation, but not necessarily the same _number_. The mini UART always appears as `/dev/ttyS0`. If you want to be specific about hardware types, use the `/dev/ttyAMA*` and `/dev/ttyS0` names.

There are also be symbolic links: `/dev/serial*`. If a UART is enabled and connected to pins 8 and 10 of the GPIO header, `/dev/serial0` will link to that UART. If a UART is enabled and connected to the onboard Bluetooth module, `/dev/serial1` links to that one. If you want to be specific about a UART connection, use the `/dev/serial*` names.

The Linux device management system chooses which hardware UARTs are connected to the GPIO pins and creates the `/dev/serial*` symlinks. By default, if there is an onboard Bluetooth module, it gets UART0 and the GPIO header gets UART1. If there is no Bluetooth, the GPIO header gets UART0. This behavior is configurable and can be changed with device tree overlays.

## Using the UARTs

### Configuring the hardware

On most devices, only UART0 is enabled by default. On compute modules, the UARTs are all disabled by default and must be explicitly enabled using a device tree overlay. You must also specify which GPIO pins to use for the interface, for example:

```
dtoverlay=uart1,txd1_pin=32,rxd1_pin=33
```

#### raspi-config

1. Start [raspi-config](raspi-config.md): `sudo raspi-config`.
1. Select option 3 - Interface Options.
1. Select option P6 - Serial Port.
1. Answer the prompts according to your needs.
1. Exit raspi-config and reboot the Pi for changes to take effect.

#### config.txt

On most devices, adding `enable-uart=1` to `/boot/config.txt` should be enough to enable the first two UART ports. On compute modules, you must also add a device-tree overlay eo enable the particular UART you want to use.

See [config.txt](config-txt/README.md) for more information.

#### Device tree overlays

Device tree overlays are also typically added in `/boot/config.txt` with lines like:
```
dtoverlay=disable-bt
```
However, device overlays are defined in the open-source [Linux source code](https://github.com/raspberrypi/linux). See [this page](device-tree.md). for further detail.

These device-tree overlays are of interest:

| Name | Purpose |
|---|---|
| disable-bt | Disable onboard Bluetooth, making UART0 available. |
| miniuart-bt | Switch the onboard Bluetooth to UART1, making UART0 available. |
| uart0 | Enable and set the pin usage of UART0 |
| uart1 | Enable and set the pin usage of UART1 |
| uart2 | Enable UART2 |
| uart3 | Enable UART3 |
| uart4 | Enable UART4 |
| uart5 | Enable UART5 |

### Serial console

Raspberry Pi OS can present a [serial console](https://en.wikipedia.org/wiki/System_console) on `/dev/serial0` and the related GPIO header pins, 8 and 10.

The serial console can be enabled by answering "Yes" to raspi-config's prompt: `Would you like a login shell to be accessible over serial?`

#### Enabling early console (earlycon) for Linux

Although the Linux kernel starts the UARTs relatively early in the boot process, it is still long after some critical bits of infrastructure have been set up. A failure in those early stages can be hard to diagnose without access to the kernel log messages from that time. That's the problem that the "earlycon" mechanism was created to work around. Consoles that support earlycon usage present an additional interface to the kernel that allows for simple, synchronous output - printk won't return until the characters have been output to the UART.

Enable earlycon with a kernel command line parameter - add one of the following to `cmdline.txt`, depending on which UART is being used as the console:
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

### Raspberry Pi as terminal

A Raspberry Pi can also act as a serial terminal, which can be used to connect to another device's serial console. You'll need to disable the terminal's serial console so that the serial console and terminal program won't conflict with each other.

To use a Raspberry Pi as a serial terminal, you can use `sudo raspi-config`, answering 'No' to the question: `Would you like a login shell to be accessible over serial?` and 'Yes' to `Would you like the serial port hardware to be enabled?`

Alternatively, you can also manually enable the UARTs and edit `/boot/cmdline.txt` to remove the portion like `console=serial0,115200`.


## Relevant differences between PL011 and mini UART

The mini UART measures time based on the CPU's core clock. If the core clock frequency is allowed to change, the mini UART's baud rate will change with it, and will not be what was intended.

Therefore, using the mini UART requires configuring the Raspberry Pi to use a fixed CPU core clock frequency. There are several ways to fix the VPU core frequency. Either setting `enable_uart=1` or `core_freq=250` in `config.txt` will work.

The mini UART also has smaller [FIFO buffers](https://en.wikipedia.org/wiki/Data_buffer#Telecommunication_buffer) than the PL011. Combined with the lack of flow control, this makes it more prone to losing characters at higher baud rates. It is also generally less capable than a PL011, mainly due to its baud rate link to the VPU clock speed.

The particular deficiencies of the mini UART compared to a PL011 are :
- No break detection
- No framing errors detection
- No parity bit
- No receive timeout interrupt
- No DCD, DSR, DTR or RI signals 

Further documentation on the mini UART can be found in the SoC peripherals document [here](../hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf).
