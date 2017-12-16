# GPIO

General Purpose Input/Output pins on the Raspberry Pi

## Overview

This page expands on the technical features of the GPIO pins available on BCM2835 in general. For usage examples, see [GPIO Usage for A+ and newer](../../../usage/gpio-plus-and-raspi2/README.md) or [GPIO Usage for models A and B](../../../usage/gpio/README.md). When reading this page, reference should be made to the BCM2835 ARM Peripherals [Datasheet](../bcm2835/README.md), section 6.

GPIO pins can be configured as either general-purpose input, general-purpose output or as one of up to 6 special alternate settings, the functions of which are pin-dependent.

There are 3 GPIO banks on BCM2835.

Each of the 3 banks has its own VDD input pin. On Raspberry Pi, all GPIO banks are supplied from 3.3V. **Connection of a GPIO to a voltage higher than 3.3V will likely destroy the GPIO block within the SoC.**

A selection of pins from Bank 0 is available on the P1 header on Raspberry Pi.

## GPIO Pads

The GPIO connections on the BCM2835 package are sometimes referred to in the peripherals datasheet as "pads" - a semiconductor design term meaning "chip connection to outside world".

The pads are configurable CMOS push-pull output drivers/input buffers. Register-based control settings are available for

- Internal pull-up / pull-down enable/disable
- Output [drive strength](http://www.scribd.com/doc/101830961/GPIO-Pads-Control2)
- Input Schmitt-trigger filtering

### Power-On States

All GPIOs revert to general-purpose inputs on power-on reset. The default pull states are also applied, which are detailed in the alternate function table in the ARM peripherals datasheet. Most GPIOs have a default pull applied.

## Interrupts

Each GPIO pin, when configured as a general-purpose input, can be configured as an interrupt source to the ARM. Several interrupt generation sources are configurable:

- Level-sensitive (high/low)
- Rising/falling edge
- Asynchronous rising/falling edge

Level interrupts maintain the interrupt status until the level has been cleared by system software (e.g. by servicing the attached peripheral generating the interrupt).

The normal rising/falling edge detection has a small amount of synchronisation built into the detection. At the system clock frequency, the pin is sampled with the criteria for generation of an interrupt being a stable transition within a 3-cycle window, i.e. a record of "1 0 0" or "0 1 1". Asynchronous detection bypasses this synchronisation to enable the detection of very narrow events.

## Alternative Functions

Almost all of the GPIO pins have alternative functions. Peripheral blocks internal to BCM2835 can be selected to appear on one or more of a set of GPIO pins, for example the I2C busses can be configured to at least 3 separate locations. Pad control, such as drive strength or Schmitt filtering, still applies when the pin is configured as an alternate function.


