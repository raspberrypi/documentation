# SPI

## Page Contents

- [Overview](#overview)  
- [Software](#software)
- [Hardware](#hardware)
- [Linux driver](#driver)
- [Troubleshooting](#troubleshooting)

<a name="overview"></a>
## Overview

The Raspberry Pi is equipped with one [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) bus that has 2 chip selects.

The SPI master driver is disabled by default on Raspbian. To enable it, use [raspi-config](../../../configuration/raspi-config.md), or ensure the line `dtparam=spi=on` isn't commented out in `/boot/config.txt`, and reboot. If the SPI driver was loaded, you should see the device `/dev/spidev0.0`.

The SPI bus is available on the P1 Header:

```
MOSI    P1-19
MISO    P1-21
SCLK    P1-23   P1-24    CE0
GND     P1-25   P1-26    CE1
```

<a name="software"></a>
## Software

### WiringPi

WiringPi includes a library which can make it easier to use the Raspberry Pi's on-board SPI interface. Accesses the hardware registers directly.

http://wiringpi.com/

### bcm2835 library

This is a C library for Raspberry Pi (RPi). It provides access to GPIO and other IO functions on the Broadcom BCM 2835 chip. Accesses the hardware registers directly.

http://www.airspayce.com/mikem/bcm2835/
### Use spidev from C

There's a loopback test program in the Linux documentation that can be used as a starting point. See the [Troubleshooting](#troubleshooting) section. Uses the Linux `spidev` driver to access the bus.

### Shell

```bash
# Write binary 1, 2 and 3
echo -ne "\x01\x02\x03" > /dev/spidev0.0
```

<a name="hardware"></a>
## Hardware

The BCM2835 on the Raspberry Pi has 3 SPI Controllers. Only the SPI0 controller is available on the header.
Chapter 10 in the [BCM2835 ARM Peripherals](../bcm2835/BCM2835-ARM-Peripherals.pdf) datasheet describes this controller.

### Master modes

Signal name abbreviations

```
SCLK - Serial CLocK
CE   - Chip Enable (often called Chip Select)
MOSI - Master Out Slave In
MISO - Master In Slave Out
MOMI - Master Out Master In
```

#### Standard mode

In Standard SPI master mode the peripheral implements the standard 3 wire serial protocol (SCLK, MOSI and MISO).

#### Bidirectional mode

In bidirectional SPI master mode the same SPI standard is implemented, except that a single wire is used for data (MOMI) instead of the two used in standard mode (MISO and MOSI). In this mode, the MOSI pin serves as MOMI pin.

#### LoSSI mode (Low Speed Serial Interface)
The LoSSI standard allows issuing of commands to peripherals (LCD) and to transfer data to and from them. LoSSI commands and parameters are 8 bits long, but an extra bit is used to indicate whether the byte is a command or parameter/data. This extra bit is set high for a data and low for a command. The resulting 9-bit value is serialized to the output. LoSSI is commonly used with [MIPI DBI](http://mipi.org/specifications/display-interface) type C compatible LCD controllers.

**Note:**

Some commands trigger an automatic read by the SPI controller, so this mode can't be used as a multipurpose 9-bit SPI.

### Transfer modes

- Polled
- Interrupt
- DMA

### Speed

The CDIV (Clock Divider) field of the CLK register sets the SPI clock speed:

```
SCLK = Core Clock / CDIV
If CDIV is set to 0, the divisor is 65536. The divisor must be a power of 2. Odd numbers rounded down. The maximum SPI clock rate is of the APB clock.
```

[Errata](http://elinux.org/BCM2835_datasheet_errata):  "must be a power of 2" probably should be "must be a multiple of 2"

See the [Linux driver](#driver) section for more info.

### Chip Select

Setup and Hold times related to the automatic assertion and de-assertion of the CS lines when operating in **DMA** mode are as follows:

- The CS line will be asserted at least 3 core clock cycles before the msb of the first byte of the transfer.
- The CS line will be de-asserted no earlier than 1 core clock cycle after the trailing edge of the final clock pulse.

<a name="driver"></a>
## Linux driver

The default Linux driver is [spi-bcm2708](https://github.com/raspberrypi/linux/blob/rpi-3.12.y/drivers/spi/spi-bcm2708.c).

The following information was valid 2014-07-05.

### Speed

The driver supports the following speeds:

```
  cdiv    speed
     2    125.0 MHz
     4     62.5 MHz
     8     31.2 MHz
    16     15.6 MHz
    32      7.8 MHz
    64      3.9 MHz
   128     1953 kHz
   256      976 kHz
   512      488 kHz
  1024      244 kHz
  2048      122 kHz
  4096       61 kHz
  8192     30.5 kHz
 16384     15.2 kHz
 32768     7629 Hz
```

When asking for say 24 MHz, the actual speed will be 15.6 MHz.

Forum post: [SPI has more speeds](https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=43442&p=347073)

### Supported Mode bits

```
SPI_CPOL    - Clock polarity
SPI_CPHA    - Clock phase
SPI_CS_HIGH - Chip Select active high
SPI_NO_CS   - 1 device per bus, no Chip Select
SPI_3WIRE   - Bidirectional mode, data in and out pin shared
```

Bidirectional or "3-wire" mode is supported by the spi-bcm2835 kernel module. Please note that in this mode, either the tx or rx field of the spi_transfer struct must be a NULL pointer, since only half-duplex communication is possible. Otherwise, the transfer will fail. The spidev_test.c source code does not consider this correctly, and therefore does not work at all in 3-wire mode.

### Supported bits per word

- 8 - Normal
- 9 - This is supported using LoSSI mode.

### Transfer modes

Only interrupt mode is supported.

### Deprecated warning

The following appears in the kernel log:

```
bcm2708_spi bcm2708_spi.0: master is unqueued, this is deprecated
```

### SPI driver latency

This [thread](https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=19489) discusses latency problems.

### DMA capable driver

This is a fork of spi-bcm2708 which enables DMA support for SPI client drivers that support DMA.

https://github.com/notro/spi-bcm2708 ([wiki](https://github.com/notro/spi-bcm2708/wiki))

<a name="troubleshooting"></a>
## Troubleshooting

### Loopback test

This can be used to test SPI send and receive. Put a wire between MOSI and MISO. It does not test CE0 and CE1.

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
