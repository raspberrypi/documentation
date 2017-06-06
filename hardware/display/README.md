# Raspberry Pi Display

## Introduction

The Raspberry Pi display is an LCD display which connects to the Raspberry Pi through the DSI connector. In some situations, it allows for the use of both the HDMI and LCD displays at the same time (this requires software support).

## Board Support

The DSI display is designed to work with Raspberry Pi models that have mounting holes in a HAT footprint. Model A/B boards are supported, but require additional mounting hardware to fit the HAT-dimensioned stand-offs on the display PCB.

### Attaching to Model A/B boards

The DSI connector on the Model A/B boards does not have the I2C connections required to talk to the touchscreen controller and DSI controller. You can work around this by using the additional set of jumper cables provided with the display kit to wire up the I2C bus on the GPIO pins to the display controller board.

Using the jumper cables, connect SCL/SDA on the GPIO header to the horizontal pins marked SCL/SDA on the display board. We also recommend that you power the Model A/B via the GPIO pins using the jumper cables.

For the GPIO header pinout, see [this diagram](http://pinout.xyz/).

DSI display autodetection is disabled by default on these boards. To enable detection, add the following line to `/boot/config.txt`:

`ignore_lcd=0`

Power the setup via the `PWR IN` micro-USB connector on the display board. Do not power the setup via the Pi's micro-USB port: the input polyfuse's maximum current rating will be exceeded as the display consumes approximately 400mA.

NB: With the display connected to the GPIO I2C pins, the GPU will assume control of the respective I2C bus. The host operating system should not access this I2C bus, as simultaneous use of the bus by both the GPU and Linux will result in sporadic crashes.

## Screen Orientation

LCD displays have an optimum viewing angle, and depending on how the screen is mounted it may be necessary to change the orientation of the display to give the best results. By default, the Raspbery Pi display and Raspberry Pi are set up to work best when viewed from slightly above, for example on a desktop. If viewing from below, you can physically rotate the display, and then tell the system software to compensate by running the screen upside down.

To flip the display, add, anywhere in the file `\boot\config.txt`, the following line:

`lcd_rotate=2`

This will vertically flip the LCD and the touch screen, compensating for the physical orientation of the display.

## Troubleshooting

Read our troubleshooting steps, tips, and tricks here: [Raspberry Pi Display Troubleshooting](troubleshooting.md).

## Specifications

- 800 x 480 RGB LCD display
- 24-bit colour
- Industrial quality: 140-degree viewing angle horizontal, 130-degree viewing angle vertical
- 10-point multi-touch touchscreen
- PWM backlight control and power control over I2C interface
- Metal-framed back with mounting points for Raspberry Pi display conversion board and Raspberry Pi
- Blacklight lifetime: 20000 hours
- Operating temperature: -20 to +70 degrees centigrade
- Storage temperature: -30 to +80 degrees centigrade
- Contrast ratio: 500
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
* [Additional drawing including radius and thickness of glass](radius.png)
