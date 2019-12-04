# Raspberry Pi 1 legacy display support

### Attaching to Model A/B boards

The DSI connector on the Model A/B boards does not have the I2C connections required to talk to the touchscreen controller and DSI controller. You can work around this by using the additional set of jumper cables provided with the display kit to wire up the I2C bus on the GPIO pins to the display controller board.

Using the jumper cables, connect SCL/SDA on the GPIO header to the horizontal pins marked SCL/SDA on the display board. We also recommend that you power the Model A/B via the GPIO pins using the jumper cables.

For the GPIO header pinout, see [this diagram](http://pinout.xyz/).

DSI display autodetection is disabled by default on these boards. To enable detection, add the following line to `/boot/config.txt`:

`ignore_lcd=0`

Power the setup via the `PWR IN` micro-USB connector on the display board. Do not power the setup via the Pi's micro-USB port: the input polyfuse's maximum current rating will be exceeded as the display consumes approximately 400mA.

NB: With the display connected to the GPIO I2C pins, the GPU will assume control of the respective I2C bus. The host operating system should not access this I2C bus, as simultaneous use of the bus by both the GPU and Linux will result in sporadic crashes.
