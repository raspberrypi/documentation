# SPI

<a name="overview"></a>
Raspberry Pi computers are equiped with a number of [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) buses. SPI can be used to connect a wide variety of peripherals - displays, network controllers (Ethernet, CAN bus), UARTs, etc. These devices are best supported by kernel device drivers, but the `spidev` API allows userspace drivers to be written in a wide array of languages.

<a name="hardware"></a>
## Hardware

The BCM2835 core common to all Raspberry Pi devices has 3 SPI Controllers:

- SPI0, with two hardware chip selects, is available on the header of all Pis (although there is an alternate mapping that is only usable on a Compute Module).

- SPI1, with three hardware chip selects, is available on Raspberry Pi computers which have a 40-pin GPIO header.

- SPI2, also with three hardware chip selects, is only usable on a Compute Module because the pins aren't brought out onto the 40-pin header.

BCM2711 adds another 4 SPI buses - SPI3 to SPI6, each with 2 hardware chip selects. All are available on the 40-pin header (provided nothing else is trying to use the same pins).

Chapter 10 in the [BCM2835 ARM Peripherals](../bcm2835/BCM2835-ARM-Peripherals.pdf) datasheet describes the main controller.  Chapter 2.3 describes the auxiliary controller.

### Pin/GPIO mappings

#### SPI0 (available on all Raspberry Pis)
| SPI function | Header pin | Broadcom pin name | Broadcom pin function |
|---|---|---|---|
| MOSI | 19 | GPIO10 | SPI0_MOSI |
| MISO | 21 | GPIO09 | SPI0_MISO |
| SCLK | 23 | GPIO11 | SPI0_SCLK |
| CE0  | 24 | GPIO08 | SPI0_CE0_N |
| CE1  | 26 | GPIO07 | SPI0_CE1_N |

#### SPI0 alternate mapping (available only on Compute Modules)
| SPI function | Broadcom pin name | Broadcom pin function |
|---|---|---|
| MOSI | GPIO38 | SPI0_MOSI |
| MISO | GPIO37 | SPI0_MISO |
| SCLK | GPIO39 | SPI0_SCLK |
| CE0  | GPIO36 | SPI0_CE0_N |
| CE1  | GPIO35 | SPI0_CE1_N |

#### SPI1 (available only on 40-pin GPIO header)
| SPI function | Header pin | Broadcom pin name | Broadcom pin function |
|---|---|---|---|
| MOSI | 38 | GPIO20 | SPI1_MOSI |
| MISO | 35 | GPIO19 | SPI1_MISO |
| SCLK | 40 | GPIO21 | SPI1_SCLK |
| CE0  | 12 | GPIO18 | SPI1_CE0_N |
| CE1  | 11 | GPIO17 | SPI1_CE1_N |
| CE2  | 36 | GPIO16 | SPI1_CE2_N |

#### SPI2 (available only on Compute Modules)
| SPI function | Broadcom pin name | Broadcom pin function |
|---|---|---|
| MOSI | GPIO41 | SPI2_MOSI |
| MISO | GPIO40 | SPI2_MISO |
| SCLK | GPIO42 | SPI2_SCLK |
| CE0  | GPIO43 | SPI2_CE0_N |
| CE1  | GPIO44 | SPI2_CE1_N |
| CE2  | GPIO45 | SPI2_CE2_N |

#### SPI3 (BCM2711 only)
| SPI function | Header pin | Broadcom pin name | Broadcom pin function |
|---|---|---|---|
| MOSI | 03 | GPIO02 | SPI3_MOSI |
| MISO | 28 | GPIO01 | SPI3_MISO |
| SCLK | 05 | GPIO03 | SPI3_SCLK |
| CE0  | 27 | GPIO00 | SPI3_CE0_N |
| CE1  | 18 | GPIO24 | SPI3_CE1_N |

#### SPI4 (BCM2711 only)
| SPI function | Header pin | Broadcom pin name | Broadcom pin function |
|---|---|---|---|
| MOSI | 31 | GPIO06 | SPI4_MOSI |
| MISO | 29 | GPIO05 | SPI4_MISO |
| SCLK | 26 | GPIO07 | SPI4_SCLK |
| CE0  | 07 | GPIO04 | SPI4_CE0_N |
| CE1  | 22 | GPIO25 | SPI4_CE1_N |

#### SPI5 (BCM2711 only)
| SPI function | Header pin | Broadcom pin name | Broadcom pin function |
|---|---|---|---|
| MOSI | 08 | GPIO14 | SPI5_MOSI |
| MISO | 33 | GPIO13 | SPI5_MISO |
| SCLK | 10 | GPIO15 | SPI5_SCLK |
| CE0  | 32 | GPIO12 | SPI5_CE0_N |
| CE1  | 37 | GPIO26 | SPI5_CE1_N |

#### SPI6 (BCM2711 only)
| SPI function | Header pin | Broadcom pin name | Broadcom pin function |
|---|---|---|---|
| MOSI | 38 | GPIO20 | SPI6_MOSI |
| MISO | 35 | GPIO19 | SPI6_MISO |
| SCLK | 40 | GPIO21 | SPI6_SCLK |
| CE0  | 12 | GPIO18 | SPI6_CE0_N |
| CE1  | 13 | GPIO27 | SPI6_CE1_N |

### Master modes

Signal name abbreviations:

- SCLK - serial clock
- CE   - chip enable (often called chip select)
- MOSI - master out slave in
- MISO - master in slave out
- MOMI - master out master in

#### Standard mode

In Standard SPI mode the peripheral implements the standard 3 wire serial protocol (SCLK, MOSI and MISO).

#### Bidirectional mode

In bidirectional SPI mode the same SPI standard is implemented, except that a single wire is used for data (MOMI) instead of the two used in standard mode (MISO and MOSI). In this mode, the MOSI pin serves as MOMI pin.

#### LoSSI (low speed serial interface) mode
The LoSSI standard allows issuing commands to peripherals, and transfering data to and from them. LoSSI commands and parameters are 8 bits long, with an extra bit used to indicate whether the byte is a command or parameter/data. The extra bit is set high for data and low for a command; the resulting 9-bit value is serialized to the output. LoSSI is commonly used with [MIPI DBI](http://mipi.org/specifications/display-interface) type C compatible LCD controllers.

**Note:** some commands trigger an automatic read by the SPI controller, so this mode cannot be used as a multipurpose 9-bit SPI.

### Transfer modes

- Polled
- Interrupt
- DMA

### Speed

The clock divider (CDIV) field of the CLK register is used to set the SPI clock speed (SCLK) using the formula:

```SCLK = core clock / CDIV```

If CDIV is set to 0, a divisor of 65536 is used in its place. CDIV must be a multiple of 2: odd numbers are rounded down. Note that not all possible clock rates are usable because of analogue electrical issues (rise times, drive strengths etc). 

See the [Linux driver](#driver) section for more info.

### Chip selects

Setup and hold times related to the automatic assertion and de-assertion of the CS lines when operating in **DMA** mode are as follows:

- The CS line will be asserted at least 3 core clock cycles before the msb of the first byte of the transfer

- The CS line will be de-asserted no earlier than 1 core clock cycle after the trailing edge of the final clock pulse

<a name="software"></a>
## Software

<a name="driver"></a>
### Linux driver

The default Linux driver is now the standard spi-bcm2835.

SPI0 is disabled by default. To enable it, use [raspi-config](../../../configuration/raspi-config.md), or ensure the line `dtparam=spi=on` isn't commented out in `/boot/config.txt`. By default it uses 2 chip select lines, but this can be reduced to 1 using `dtoverlay=spi0-1cs`. `dtoverlay=spi0-2cs` also exists, and without any parameters it is equivalent to `dtparam=spi=on`.

To enable SPI1, you can use 1, 2 or 3 chip select lines, adding in each case:
<pre>
dtoverlay=spi1-1cs  #1 chip select
dtoverlay=spi1-2cs  #2 chip select
dtoverlay=spi1-3cs  #3 chip select
</pre>
to /boot/config.txt file. Similar overlays exist for SPI2, SPI3, SPI4, SPI5 and SPI6.

The driver does not make use of the hardware chip select lines because of some limitations - instead it can use an arbitrary number of GPIOs as software/GPIO chip selects. This means you are free to choose any spare GPIO as a CS line, and all of these SPI overlays include that control - see `/boot/overlays/README` for details, or run (for example) `dtoverlay -h spi0-2cs` (`dtoverlay -a | grep spi` might be helpful to list them all).

#### Speed

The driver supports all speeds which are even integer divisors of the core clock, although as noted above not all of these speeds will support data transfer due to limits in the GPIOs and in the devices attached. As a rule of thumb, anything over 50MHz is unlikely to work, but your mileage may vary.

#### Supported mode bits

| bit | description |
|-----|-------------|
| SPI_CPOL | clock polarity |
| SPI_CPHA | clock phase |
| SPI_CS_HIGH | chip select active high |
| SPI_NO_CS | 1 device per bus, no chip select |
| SPI_3WIRE | bidirectional mode, data in and out pin shared |

Bidirectional, or 3-wire, mode is supported by the spi-bcm2835 kernel module. Please note that in this mode, either the TX or RX field of the `spi_transfer` struct must be a NULL pointer, since only half-duplex communication is possible: Otherwise, the transfer will fail. The `spidev_test.c` code does not consider this correctly, and therefore does not work at all in 3-wire mode.

#### Supported bits per word

- 8 - Normal
- 9 - LoSSI mode only

#### Transfer modes

Interrupt mode is supported on all SPI buses. SPI0, and SPI3-6 also support DMA transfers.

#### SPI driver latency

This [thread](https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=19489) discusses latency problems.

### spidev

The `spidev` API presents an ioctl-based userspace interface to individual SPI CS lines. Device tree is used to indicate whether a CS line is going to be driven by a kernel driver module or managed by `spidev` on behalf of the user; it isn't possible to do both at the same time. Note that Raspberry Pi's own kernels are more relaxed about the use of device tree to enable `spidev` - the upstream kernels print warnings about such usage, and ultimately may prevent it altogether.

#### Using spidev from C

There's a loopback test program in the Linux documentation that can be used as a starting point. See the [Troubleshooting](#troubleshooting) section.

#### Using spidev from Python

There are several Python libraries that provide access to `spidev`, including the imaginatively named `spidev` (`pip install spidev` - see https://pypi.org/project/spidev/) and `SPI-Py` (https://github.com/lthiery/SPI-Py).

#### Using spidev from shell

Example: write binary 1, 2 and 3 using bash: 

```bash
echo -ne "\x01\x02\x03" > /dev/spidev0.0
```

### Other SPI libraries

There are other userspace libraries that provide SPI control by directly manipulating the hardware. This is not recommended.

<a name="troubleshooting"></a>
## Troubleshooting

### Loopback test

This can be used to test SPI send and receive: put a wire between MOSI and MISO. It does not test CE0 and CE1.

```bash
wget https://raw.githubusercontent.com/raspberrypi/linux/rpi-3.10.y/Documentation/spi/spidev_test.c
gcc -o spidev_test spidev_test.c
./spidev_test -D /dev/spidev0.0
spi mode: 0
bits per word: 8
max speed: 500000 Hz (500 KHz)

FF FF FF FF FF FF
40 00 00 00 00 95
FF FF FF FF FF FF
FF FF FF FF FF FF
FF FF FF FF FF FF
DE AD BE EF BA AD
F0 0D
```

Some of the content above has been copied from [https://elinux.org/RPi_SPI](the elinux SPI page), which also borrows from here. Both are covered by the CC-SA license.
