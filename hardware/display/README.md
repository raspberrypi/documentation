# Raspberry Pi Display

## Introduction

The Raspberry Pi display is an LCD display which connects to the Raspberry Pi through the DSI connector, it allows the use of both the HDMI and LCD displays at the same time in some situations (this implies requiring software support)

## Board Support

The DSI display is designed to work with Raspberry Pi models that have mounting holes in a HAT footprint. Model A/B boards are supported, but require additional mounting hardware to fit the HAT-dimensioned stand-offs on the display PCB.

### Attaching to Model A/B boards

The DSI connector on Model A/B boards does not have the I2C connections required to talk to the touchscreen controller and DSI controller. This can be worked around by using the additional set of jumpers provided with the display kit to wire up the I2C bus on the GPIO pins to the display controller board.

Using the wire jumpers, connect SCL/SDA on the GPIO header to the horizontal pins marked SCL/SDA on the display board. It is also recommended to power the Model A/B via the GPIO pins using the jumpers.

For the GPIO header pinout, see this diagram: http://pinout.xyz/

DSI display autodetection is disabled by default on these boards. To enable detection, add the following line to /boot/config.txt:

`ignore_lcd=0`

Power the setup via the PWR IN micro-USB connector on the Display board. Do not power the setup via the Pi's micro-USB port: the input polyfuse's maxiumum current rating will be exceeded as the display consumes approximately 400mA.

NB: With the display connected to the GPIO I2C pins, the GPU will assume control of the respective I2C bus. The host operating system should not access this I2C bus as simultaneous use of the bus by both the GPU and Linux will result in sporadic crashes.

## Troubleshooting

Read our troubleshooting steps, tips and tricks here: [Raspberry Pi Display Troubleshooting](troubleshooting.md)

## Specifications

* 800x480 RGB LCD display
* 24 bit colour
* Industrial quality, 140 degree viewing angle horizontal, 130 degree vertical
* 10 point multi-touch touchscreen
* PWM backlight control and power control over I2C interface
* Metal framed back with mounting points for Raspberry pi display conversion board and Raspberry Pi
* Blacklight lifetime: 20000 hours
* Operating temperature: -20 to +70 degrees centigrade
* Storage temperature: -30 to +80 degrees centigrade
* Contrast ratio: 500
* Average brightness: 250 cd/m<sup>2</sup>
* Viewing angle (degrees):
  * Top - 50
  * Bottom - 70
  * Left - 70
  * Right - 70

## Module mechanical specification

* Outer dimensions: 192.96 x 112.76mm
* Viewable area: 154.08 x 85.92mm
* [Download mechanical drawing (PDF, 592kb)](7InchDisplayDrawing-14092015.pdf)
