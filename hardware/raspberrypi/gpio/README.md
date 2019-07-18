# GPIO

General Purpose Input/Output pins on the Raspberry Pi

## Overview

This page expands on the technical features of the GPIO pins available on BCM2835 in general. For usage examples, see [GPIO usage ](../../../usage/gpio/README.md). When reading this page, reference should be made to the BCM2835 ARM peripherals [data sheet](../bcm2835/README.md), section 6.

GPIO pins can be configured as either general-purpose input, general-purpose output, or as one of up to six special alternate settings, the functions of which are pin-dependent.

There are three GPIO banks on BCM2835.

Each of the three banks has its own VDD input pin. On Raspberry Pi, all GPIO banks are supplied from 3.3V. **Connection of a GPIO to a voltage higher than 3.3V will likely destroy the GPIO block within the SoC.**

A selection of pins from Bank 0 is available on the P1 header on Raspberry Pi.

## GPIO pads

The GPIO connections on the BCM2835 package are sometimes referred to in the peripherals data sheet as "pads" — a semiconductor design term meaning 'chip connection to outside world'.

The pads are configurable CMOS push-pull output drivers/input buffers. Register-based control settings are available for:

- Internal pull-up / pull-down enable/disable
- Output [drive strength](gpio_pads_control.md)
- Input Schmitt-trigger filtering

### Power-on states

All GPIO pins revert to general-purpose inputs on power-on reset. The default pull states are also applied, which are detailed in the alternate function table in the ARM peripherals datasheet. Most GPIOs have a default pull applied.

## Interrupts

Each GPIO pin, when configured as a general-purpose input, can be configured as an interrupt source to the ARM. Several interrupt generation sources are configurable:

- Level-sensitive (high/low)
- Rising/falling edge
- Asynchronous rising/falling edge

Level interrupts maintain the interrupt status until the level has been cleared by system software (e.g. by servicing the attached peripheral generating the interrupt).

The normal rising/falling edge detection has a small amount of synchronisation built into the detection. At the system clock frequency, the pin is sampled with the criteria for generation of an interrupt being a stable transition within a three-cycle window, i.e. a record of '1 0 0' or '0 1 1'. Asynchronous detection bypasses this synchronisation to enable the detection of very narrow events.

## Alternative functions

Almost all of the GPIO pins have alternative functions. Peripheral blocks internal to BCM2835 can be selected to appear on one or more of a set of GPIO pins, for example the I2C busses can be configured to at least 3 separate locations. Pad control, such as drive strength or Schmitt filtering, still applies when the pin is configured as an alternate function.

## Voltage specifications

The following table gives the various voltage specifications for the GPIO pins, it was extracted from the Compute Module datasheet [here](../../computemodule/datasheet.md).

| Symbol | Parameter | Conditions &emsp;| Min | Typical | Max | Unit |
|--------|-----------|------------|------|---------|------|------|
|V<sub>IL</sub>|Input Low Voltage | VDD IO = 1.8V | - | - |0.6  | V |
| | | VDD IO = 2.7V | - | - | 0.8 | V |
| | | VDD IO = 3.3V | - | - | 0.9 | V |
|V<sub>IH</sub>| Input high voltage<sup>a</sup> | VDD IO = 1.8V | 1.0 | - | - | V |
| | | VDD IO = 2.7V | 1.3 | - | - | V |
| | |VDD IO = 3.3V | 1.6 | - | - | V |
|I<sub>IL</sub>| Input leakage current | TA = +85◦C | - | - | 5 | µA |
|C<sub>IN</sub>| Input capacitance | - | - | 5 | - | pF |
|V<sub>OL</sub>| Output low voltage<sup>b</sup> | VDD IO = 1.8V, IOL = -2mA | - | - | 0.2 | V |
| | | VDD IO = 2.7V, IOL = -2mA | - | - | 0.15 | V |
| | | VDD IO = 3.3V, IOL = -2mA | - | - | 0.14 | V |
|V<sub>OH</sub>| Output high voltage<sup>b</sup> | VDD IO = 1.8V, IOH = 2mA | 1.6 | - | - | V |
| | | VDD IO = 2.7V, IOH = 2mA | 2.5 | - | - | V |
| | | VDD IO = 3.3V, IOH = 2mA | 3.0 | - | - | V |
|I<sub>OL</sub>| Output low current<sup>c</sup> | VDD IO = 1.8V, VO = 0.4V | 12 | - | - | mA |
| | | VDD IO = 2.7V, VO = 0.4V | 17 | - | - | mA |
| | | VDD IO = 3.3V, VO = 0.4V | 18 | - | - | mA | 
|I<sub>OH</sub>| Output high current<sup>c</sup> | VDD IO = 1.8V, VO = 1.4V | 10 | - | - | mA | 
| | | VDD IO = 2.7V, VO = 2.3V | 16 | - | - | mA | 
| | | VDD IO = 3.3V, VO = 2.3V | 17 | - | - | mA | 
| R<sub>PU</sub> | Pullup resistor | - | 50 | - | 65 | kΩ |
| R<sub>PD</sub> | Pulldown resistor | - | 50 | - |65 | kΩ | 

<sup>a</sup> Hysteresis enabled  
<sup>b</sup> Default drive strength (8mA)  
<sup>c</sup> Maximum drive strength (16mA)
