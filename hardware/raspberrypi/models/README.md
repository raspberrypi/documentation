# Raspberry Pi Models and Revisions

## Page Contents

- [Overview](#overview)
- [The Model B+](#modelbplus)
- [The Model A+](#modelaplus)
- [The Model B](#modelb)
- [The Model A](#modela)
- [The Compute Module](#computemodule)

<a name="overview"></a>
## Overview

This page describes the models of Raspberry Pi available. It does not attempt to provide full specifications, and is intended as an overview in order to help prospective purchasers make a decision as to which device they need.

There are currently five Raspberry Pi models. They are the [Model B+](http://www.raspberrypi.org/product/model-b-plus/), the [Model A+](http://www.raspberrypi.org/products/model-a-plus/), the [Model B](http://www.raspberrypi.org/products/model-b/), the [Model A](http://www.raspberrypi.org/products/model-a/), and the Compute Module (currently only available as part of the [Compute Module development kit](http://www.raspberrypi.org/products/compute-module-development-kit/) ). All models use the same SoC (System on Chip - combined CPU & GPU), the [BCM2835](../bcm2835/README.md), but other hardware features differ.

The A and B use the same PCB, whilst the B+ and A+ are a new design but of very similar form factor. The Compute Module is an entirely different form factor and cannot be used standalone.

For a table comparing the specifications of each model, see [here](specs.md)

<a name="modelbplus"></a>
## Model B+

Released in July 2014, the Model B+ is an updated revision of the Model B. It increases the number of USB ports to 4 and the number of pins on the GPIO header to 40. In addition, it has improved power circuitry which allows higher powered USB devices to be attached and now hot-plugged. The full size composite video connector has been removed and the functionality moved to the 3.5mm audio/video jack. The full size SD card slot has also been replaced with a much more robust microSD slot.

The following list details some of the improvements over the Model B.

 - Current monitors on the USB ports mean the B+ now supports hot-plugging
 - Current limiter on the 5V for HDMI means HDMI cable-powered VGA converters will now all work
 - 14 more GPIO pins
 - EEPROM readout support for the new [HAT](http://www.raspberrypi.org/introducing-raspberry-pi-hats/) expansion boards
 - Higher drive capacity for analog audio out, from a separate regulator, which means a better audio DAC quality
 - No more backpowering problems, due to the USB current limiters which also inhibit back flow, together with the "ideal power diode"
 - Composite output moved to 3.5mm jack
 - Connectors now moved to two sides of the board rather than the four of the original device
 - Ethernet LEDs moved to the ethernet connector
 - 4 squarely-positioned mounting holes for more rigid attachement to cases etc.

The power circuit changes also means a reduction in power requirements of between 0.5W and 1W.

### Revisions

There have been a number of revison changes over the lifetime of the Model B; and the B+, despite its dramatic improvements over the B, is simply a new revision, and is expected to be the final one using the BCM2835. It is in effect revision 3 of the board. 

Revision 1 is the revision as of initial launch, whilst revision 2 improved the power and USB circuitry to increase reliability, and also included 2 registration holes that could also be used for mounting the device. There have also been minor revision changes during the lifetime of the board to help wth manufacture, testing, and production line BOM (Bill of material) transitions.

<a name="modelaplus"></a>
## Model A+

Released in November 2014, this is the 'plus' variant of the Model A. It has 40 GPIO pins, a single USB port, no ethernet and 256MB of SDRAM. It also has a smaller form factor than the other models measuring 65mm in length.

<a name="modelb"></a>
## Model B

Until July 2014, this was the top end device. It has two USB ports, and 512MB of SDRAM. Note, early versions of the board had 256MB of SDRAM.

Additional ports included over the Model A specification are:

 - One ethernet port

<a name="modela"></a>
## Model A

This is the basic device, with a single USB port and 256MB of SDRAM. Onboard ports include:

 - Full size SD card
 - HDMI output port
 - Composite video output
 - One USB port
 - 26 pin expansion header exposing GPIO, I2C etc
 - 3.5mm audio jack
 - Camera interface port (CSI-2)
 - LCD display interface port (DSI)
 - One microUSB power connector for powering the device

Beause there is no ethernet or extra USB ports on this device, it has a lower power comsumption than the Model B/B+.
 - Two USB ports

<a name="computemodule"></a>
## Compute Module

The compute module is intended for industrial applications, it is a cut down device which simply includes the BCM2835, 512MB of SDRAM and a 4GB eMMC flash memory, in a small form factor. This connects to a base board using a repurposed 200 pin DDR2 SODIMM connector. Note the device is NOT SODIMM compatible, it just repurposes the connector. All the BCM2835 features are exposed via the SODIMM connector, including twin camera and LCD ports, whilst the Model A or B/B+ only have one of each.

The compute module is expected to be used by companies wishing to shortcut the development process of new product, meaning only a baseboard needs to be developed, with appropriate peripherals, with the Compute Module providing the CPU, memory and storage along with tested and reliable software.
