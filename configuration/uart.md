# UART configuration

A [UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) is a serial communication device which uses one or more signal wires and a common ground to transmit and receive data between two devices. When computer people talk about 'serial ports', they usually mean UARTs. People from DOS/Windows background may know these as 'COM ports'.

## Hardware

On all Raspberry Pi computers except microcontrollers, there are at least two UARTs built into the [SoC](https://en.wikipedia.org/wiki/System_on_a_chip). The Raspberry Pi 4 family has six UARTs.

There are also two different types of UART devices available on the Raspberry Pi:
* [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) part of the ARM spec and is patterned on the full-featured [16550 UART](https://en.wikipedia.org/wiki/16550_UART) chip.
* mini UART is patterned on the slightly older and less full-featured [8250 UART](https://en.wikipedia.org/wiki/8250_UART) chip.

The naming/numbering of the UARTs can be confusing because they are listed one way in the Broadcom SoC documentation, and another way in Linux. Depending on the board features and configuration, either of the first two UARTs may appear on the same pins in the GPIO header, so you they aren't uniquely described by their locations either.

Broadcom gives each UART a name and number in their SoC documentation, and this is a good starting point.

| SoC | UART0 | UART1 | UART2 | UART3 | UART4 | UART5 |
| --- | --- | --- | --- | --- | --- | --- |
| BCM2835 | PL011 | mini UART |
| BCM2836 | PL011 | mini UART |
| BCM2837 | PL011 | mini UART |
| BCM2711 | PL011 | mini UART | PL011 | PL011 | PL011 | PL011 |

 See the [Raspberry Pi 4 Model B Datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711/rpi_DATA_2711_1p0_preliminary.pdf) section _5.1.2 GPIO Alternate Functions_, for details on exactly which UART can appear on which GPIO numbers. Earlier models are similar, but have only the first two UARTs. Take care to line up the numbers: TXD0 and RXD0 always belong to UART0, TXD1 to UART1 and so on. Also, remember that the GPIO numbering is on the CPU, and is different than the GPIO pin numbers on the 40-pin J8 header.

Inside the Raspberry Pi, the UARTs are able to connect in several ways. UART0 and UART1 can connect to either the GPIO lines or the onboard Bluetooth module, if there is one. UARTs two through five connect to the GPIO lines and nowhere else.

### Voltages

All the onboard Raspberry Pi UARTs are 3.3V [logic level](https://en.wikipedia.org/wiki/Logic_level) only, sometimes called ['CMOS'](https://en.wikipedia.org/wiki/CMOS) level. Do not connect Raspberry Pi UARTs to 5V circuits, sometimes called ['TTL'](https://en.wikipedia.org/wiki/Transistor%E2%80%93transistor_logic) level, because the Raspberry Pi will be damaged. [RS-232](https://en.wikipedia.org/wiki/RS-232) uses +/- 12V signals, which are right out.

There are chips called ['level shifters'](https://en.wikipedia.org/wiki/Level_shifter) which convert voltages between levels. You can find them either as individual ICs for using in your own designs, or integrated into other devices to make them compatible. They're inexpensive and readily available from third parties.

## Software support

Raspberry Pi OS has built-in drivers for the UARTs built into the SoC, and common external types as well.

The PL011 devices will appear as [character devices](https://en.wikipedia.org/wiki/Device_file#Character_devices) with names like `/dev/ttyAMA*`. If there are multiple PL011s, they're in the same _order_ as the Broadcom documentation, but not necessarily the same _number_. The mini UART always appears as character device named `/dev/ttyS0`, and there is never more than one. If you want to be specific about which hardware type you're using, use the `/dev/ttyAMA*` and `/dev/ttyS0` names.

There are also be symbolic links with names like `/dev/serial*`. If a UART is enabled and configured to appear on pins 8 and 10 of the GPIO header, `/dev/serial0` will link to that UART. If a UART is enabled and configured to connect to the onboard Bluetooth module, `/dev/serial1` links to that one. If you want to be specific about where a UART is connected, use the `/dev/serial*` names.

The Linux device management system chooses which hardware UARTs are connected to the GPIO pins and creates the `/dev/serial*` symlinks. By default, if there is an onboard Bluetooth module, it gets UART0 and the GPIO header gets UART1. If there is no Bluetooth, the GPIO header gets UART0. This behavior is configurable and can be changed with device tree overlays.

## Using the UARTs

### Configuring the hardware

There are several ways to configure the UART hardware.

#### raspi-config

1. Start [raspi-config](raspi-config.md): `sudo raspi-config`.
1. Select option 3 - Interface Options.
1. Select option P6 - Serial Port.
1. Answer the prompts according to your needs.
1. Exit raspi-config and reboot the Pi for changes to take effect.

#### config.txt

Adding `enable-uart=1` to `/boot/config.txt` should be enough to enable the first two UART ports.

See [config.txt](config-txt/README.md) for more information.

#### Device tree overlays

Device tree overlays are also typically added in `/boot/config.txt` with lines like:
```
dtoverlay=disable-bt
```
However, device overlays are defined in the open-source [Linux source code](https://github.com/raspberrypi/linux). By contrast, the options available in config.txt are defined by the closed-source bootloader from Raspberry Pi and Broadcom. For full instructions on how to use Device Tree overlays see [this page](device-tree.md). Note that the `-overlay.dts` part of the filenames are removed.

You can list the available device-tree overlays by running `dtoverlay -a`. Refer to `/boot/overlays/README` for details on Device Tree overlays, or run `dtoverlay -h overlay-name` for descriptions and usage information.

These device-tree overlays are of interest:

| Name | Purpose |
|---|---|
| disable-bt | Disable onboard Bluetooth, making UART0 available. |
| miniuart-bt | Switch the onboard Bluetooth to UART1, making UART0 available. |
| uart0 | Change the pin usage of UART0 |
| uart1 | Change the pin usage of UART1 |
| uart2 | Enable UART2 |
| uart3 | Enable UART3 |
| uart4 | Enable UART4 |
| uart5 | Enable UART5 |

### Serial console

If configured, Raspberry Pi OS can present a login prompt and some system messages on `/dev/serial0` and the related GPIO header pins, 8 and 10. This arrangement is called a ['serial console'](https://en.wikipedia.org/wiki/System_console) and is a traditional way to access a computer that may not have its own human-interface hardware such as a keyboard, monitor, etc. For example, many network servers have serial consoles.

The serial console can be enabled and disabled by answering "Yes" to raspi-config's prompt: `Would you like a login shell to be accessible over serial?`

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

A device you use to login to a serial console is called a ['terminal'](https://en.wikipedia.org/wiki/Computer_terminal). A Raspberry Pi can also act as a terminal, so you can actually login from one Raspberry Pi to another with just a few wires and no network! You just need to connect the two devices' grounds together, and then connect one's TXD to the other's RXD, and vice versa. No resistors or other special hardware are required.

Regardless of whether you're connecting to another Raspberry Pi or some other device, if you're going to use your Raspberry Pi as a terminal, you'll need to disable its serial console. Otherwise, your Raspberry Pi's own serial console will conflict with the terminal program.

`sudo raspi-config` disables the serial console but leaves the serial port enabled if you answer 'No' to the question: `Would you like a login shell to be accessible over serial?` and 'Yes' to `Would you like the serial port hardware to be enabled?`

You can also manually edit `/boot/cmdline.txt` and remove the portion like `console=serial0,115200`. Don't mess with the part that says `console=tty1`－that says to output system messages to the video output.

Regardless of which method you use, you will need to be root or use `sudo` to change the settings, and reboot to let the changes take effect.

There are a few programs that can open the serial port for you. These are called  ['terminal emulators'](https://en.wikipedia.org/wiki/Computer_terminal#Emulation). A simple one is called 'screen'.

To install screen, run:
```shell
sudo apt update
sudo apt install screen
```

With screen installed, you can run `screen /dev/serial0` to open the serial port. `CTRL-C` doesn't kill the terminal program, as it does most other programs. If it did, when you tried to kill a program on the remote computer, you'd accidentally kill your connection instead. So screen passes `CTRL-C` on to the remote computer. To close the connection and quit screen, press `CTRL-A` and then `k` (for kill) and confirm with `y`. For help, press `CTRL-A ?`.

N.B: screen and any other terminal emulator show only the data that comes in through the UART. Therefore, the screen will be blank if there's no one on the other end of the line, or if they haven't transmitted anything.

## Relevant differences between PL011 and mini UART

UARTs work by raising and lowering voltages with very precise timing, called the 'baud rate'. The mini UART measures time based on the CPU's core clock. If the core clock frequency is allowed to change, the mini UART's baud rate will change with it, and will not be what was intended.

Therefore, using the mini UART requires configuring the Raspberry Pi to use a fixed CPU core clock frequency. There are several ways to fix the VPU core frequency. Either setting `enable_uart=1` or `core_freq=250` in `config.txt` will work.

The mini UART also has smaller [FIFO buffers](https://en.wikipedia.org/wiki/Data_buffer#Telecommunication_buffer) than the PL011. Combined with the lack of flow control, this makes it more prone to losing characters at higher baud rates. It is also generally less capable than a PL011, mainly due to its baud rate link to the VPU clock speed.

The particular deficiencies of the mini UART compared to a PL011 are :
- No break detection
- No framing errors detection
- No parity bit
- No receive timeout interrupt
- No DCD, DSR, DTR or RI signals 

Further documentation on the mini UART can be found in the SoC peripherals document [here](../hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf).
