# UARTs on the Raspberry Pi

There are two types of UART available on the Raspberry Pi -  [PL011](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0183g/index.html) and mini UART. The PL011 is a capable, broadly 16550-compatible UART, while the mini UART has a reduced feature set.

All UARTs on the Raspberry Pi are 3.3V only - damage will occur if they are connected to 5V systems. An adaptor can be used to connect to 5V systems. alternatively, low-cost USB to 3.3V serial adaptors are available from various third parties.

## Pi Zero, 1, 2 and 3 - two UARTs

The Raspberry Pi Zero, 1, 2 and 3 each contain two UARTs as follows:

| Name | Type |
|------|------|
|UART0 |PL011 |
|UART1 |mini UART |

## Pi 4 - six UARTS

The Raspberry Pi 4 has four additional PL011s:

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

The secondary UART is not normally present on the GPIO connector. By default, the secondary UART is connected to the Bluetooth side of the combined wireless LAN/Bluetooth controller, on models to which this is fitted.

## Configuration

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
|`/dev/serial0` |primary UART |
|`/dev/serial1` |secondary UART |

Note: `/dev/serial0` and `/dev/serial1` are symbolic links which point to either `/dev/ttyS0` or `/dev/ttyAMA0`.

## Mini UART and CPU core frequency

In order to use the mini UART, you need to configure the Raspberry Pi to use a fixed VPU core clock frequency. This is because the mini UART clock is linked to the VPU core clock, so that when the core clock frequency changes, the UART baud rate will also change. The `enable_uart` and `core_freq` settings can be added to `config.txt` to change the behaviour of the mini UART. The following table summarises the possible combinations:

| Mini UART set to | core clock | Result |
|------------------|------------|--------|
| primary UART     | variable   | mini UART disabled |
| primary UART     | fixed by setting `enable_uart=1` | mini UART enabled, core clock fixed to 250MHz, or if `force_turbo` is set, the VPU turbo frequency |
| secondary UART   | variable   | mini UART disabled |
| secondary UART   | fixed by setting `core_freq=250` | mini UART enabled |

The default state of the `enable_uart` flag depends on which UART is the primary UART:

| Primary UART | Default state of enable_uart flag |
|--------------|-----------------------------------|
| mini UART    | 0 |
| PL011        | 1 |

## Disable Linux serial console

By default, the primary UART is assigned to the Linux console. If you wish to use the primary UART for other purposes, you must reconfigure Raspbian. This can be done by using [raspi-config](raspi-config.md):

1. Start raspi-config: `sudo raspi-config`.
1. Select option 5 - interfacing options.
1. Select option P6 - serial.
1. At the prompt `Would you like a login shell to be accessible over serial?` answer 'No'
1. At the prompt `Would you like the serial port hardware to be enabled?` answer 'Yes'
1. Exit raspi-config and reboot the Pi for changes to take effect.

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
