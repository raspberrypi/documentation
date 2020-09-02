# SPI

## Page Contents

- [Overview](#overview)  
- [Hardware](#hardware)
- [Software](#software)
- [Linux driver](#driver)
- [Troubleshooting](#troubleshooting)

<a name="overview"></a>
## Overview

The Raspberry Pi family of devices is equipped with three [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) buses. The main SPI interface is referred to as SPI0 in the documentation; the second is SPI1. SPI2 is only usable on a Compute Module or Compute Module 3. By default each SPI bus has 2-3 chip selects, but this number can be changed.

<a name="hardware"></a>
## Hardware

The BCM2835 on the Raspberry Pi has 3 [http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus SPI] Controllers. The main SPI (with two slave selects) is available on the header of all Pis with Linux kernel support. The second SPI (with the option of up to three slave selects) is available on 40-pin versions of Pis, with kernel support from Raspbian Jessie 2016-05-10 distribution and up.

Chapter 10 in the [http://www.raspberrypi.org/wp-content/uploads/2012/02/BCM2835-ARM-Peripherals.pdf BCM2835 ARM Peripherals] datasheet describes the main controller.  Chapter 2.3 describes the auxiliary controller.

### Pin/GPIO mappings

#### SPI0 (available on J8/P1 headers on all RPi versions)
| SPI Function | Header Pin | Broadcom Pin Name | Broadcom Pin Name |
|---|---|---|---|
| MOSI | 19 | GPIO10 | SPI0_MOSI |
| MISO | 21 | GPIO09 | SPI0_MISO |
| SCLK | 23 | GPIO11 | SPI0_SCLK |
| CE0  | 24 | GPIO08 | SPI0_CE0_N |
| CE1  | 26 | GPIO07 | SPI0_CE1_N |

#### SPI1 (available only on 40-pin J8 header)
| SPI Function | Header Pin | Broadcom Pin Name | Broadcom Pin Name |
|---|---|---|---|
| MOSI | 38 | GPIO20 | SPI1_MOSI |
| MISO | 35 | GPIO19 | SPI1_MISO |
| SCLK | 40 | GPIO21 | SPI1_SCLK |
| CE0  | 12 | GPIO18 | SPI1_CE0_N |
| CE1  | 11 | GPIO17 | SPI1_CE1_N |
| CE2  | 36 | GPIO16 | SPI1_CE2_N |

#### SPI3 (available only on Compute Modules)
| SPI Function | Broadcom Pin Name | Broadcom Pin Name |
|---|---|---|
| MOSI | GPIO41 | SPI2_MOSI |
| MISO | GPIO40 | SPI2_MISO |
| SCLK | GPIO42 | SPI2_SCLK |
| CE0  | GPIO43 | SPI2_CE0_N |
| CE1  | GPIO44 | SPI2_CE1_N |
| CE2  | GPIO45 | SPI2_CE2_N |

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
If CDIV is set to 0, the divisor is 65536. The divisor must be a multiple of 2. Odd numbers rounded down. The maximum SPI clock rate is of the APB clock.
```

See the [Linux driver](#driver) section for more info.

### Chip Selects

Setup and Hold times related to the automatic assertion and de-assertion of the CS lines when operating in **DMA** mode are as follows:

- The CS line will be asserted at least 3 core clock cycles before the msb of the first byte of the transfer.
- The CS line will be de-asserted no earlier than 1 core clock cycle after the trailing edge of the final clock pulse.

<a name="software"></a>
## Software

The SPI master driver is disabled by default on Raspberry Pi OS. To enable it, use [raspi-config](../../../configuration/raspi-config.md), or ensure the line `dtparam=spi=on` isn't commented out in `/boot/config.txt`, and reboot. If the SPI driver was loaded, you should see the device `/dev/spidev0.0`.

<a name="driver"></a>
## Linux driver

The default Linux driver is now the standard spi-bcm2835.

SPI0 is disabled by default. To enable manually you must add `dtparam=spi=on` to `/boot/config.txt`. By default it uses 2 chip select lines, but this can be reduced to 1 using `dtoverlay=spi0-1cs`. `dtoverlay=spi0-2cs` also exists, and without any parameters it is equivalent to `dtparam=spi=on`.

To enable SPI1, you can use 1, 2 or 3 chip select lines, adding in each case:
<pre>
dtoverlay=spi1-1cs  #1 chip select
dtoverlay=spi1-2cs  #2 chip select
dtoverlay=spi1-3cs  #3 chip select
</pre>
to /boot/config.txt file. Similar overlays exist for SPI2.

All of these SPI overlays allow the chip select GPIOs to be changed - see `/boot/overlays/README` for details, or run (for example) `dtoverlay -h spi0-2cs`.

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

Interrupt mode is supported on all SPI buses. SPI0 also supports DMA transfers.

### SPI driver latency

This [thread](https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=19489) discusses latency problems.

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

Some of the content above has been copied from [https://elinux.org/RPi_SPI](the elinux SPI page), which also borrows from here. Both are covered by the CC-SA license.
