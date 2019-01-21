# GPIO pads control

This document explains the current capabilities of the Raspberry Pi GPIO pins. It is applicable to all models upto and including the Model 3B+. The main thing to note is that the GPIO drive strengths do not indicate a maximum current, but a maximum current under which the pad will still meet the specification. You should set the GPIO drive strengths to match the device being attached in order for the device to work correctly. 

#### How drive strength is controlled

Inside the pad there are a number of drivers, all in parallel. If the drive strength is set low (000) most of these are tri-stated so they do not add anything to the output current. If the drive strength is increased, more and more drivers are put in parallel. The following diagram shows that behaviour:

![GPIO Drive Strength Diagram](./images/pi_gpio_drive_strength_diagram.png)

#### What does the current value mean?

*The current value specifies the maximum current under which the pad will
still meet the specification*.

1. It is **not**: the current that the pad will deliver.
1. It is **not**: a current limit so the pad will not blow up.

The pad output is a voltage source,

* if set high the pad will try to drive the output to the rail voltage which on the Raspberry-Pi is 3V3 (3.3 Volts)
* if set low the pad will try to drive the output to ground (0 Volts)

The pad will try to drive the output high or low. Success will depend on the requriements of what is connected. If the pad is shorted to ground it will not be able to drive high. It will actually try to deliver as much current as it can and the current is only limited by the internal resistance.

If the pad is driven high and it is shorted to ground in due time it will fail! The same holds true if you connect it to 3V3 and drive it low.

Coming back to the statement that the current value specifies the maximum current under which the pad will still meet the specification.
This has to do with the guaranteed voltage levels. As this is a digital pad there are two voltage levels, high and low. Yet how high and how low? Is high 0.9V or 1.5V or 2.7V or some other voltage?

To answer that question I/O ports have two parameters which deal with the output level:
*  V<sub>IL</sub>: The maximum low level voltage. (0.8V on the BCM2835/6/7)
*  V<sub>IH</sub> : The minimum high level voltage. (1.3V on the BCM2835/6/7)

V<sub>IL</sub>=0.8V means that if the output is Low it will be <= 0.8V.
V<sub>IL</sub>=1.3V means that if the output is High it will be >= 1.3V.
   
Thus a drive strength of 16mA means:

If you set the pad high you can draw up to 16mA and it is guaranteed that the output voltage will be >=1.3V. This also means that if you set a drive strength of 2mA and you draw 16mA the voltage will **not** be 1.3 Volt but lower. In fact it may not be high enough to be seen as high by an external device.

#### Why don't I set all my pads to the maximum current?

Two reasons:

1. The Raspberry Pi 3V3 supply was designed with a maximum current of ~3mA per GPIO pin. If you load each pin with 16mA the total current is 272mA. The 3V3 supply will collapse under that level of load.
1. Big current spikes will happen especially if you have a capacitive load. That will "bounce" around all the other pins near it. It is likely to cause interference with the SD-card or even the SDRAM behaviour.

#### What is a safe current?

All the electronics of the pads are designed for 16mA. That is a safe value under which you will not damage the device. Even if you set the drive strength to 2mA and then load it so 16mA comes out that will not damage the device. Other than that there is no guaranteed maximum safe current.

### GPIO Addresses

* 0x 7e10 002c PADS (GPIO 0-27)
* 0x 7e10 0030 PADS (GPIO 28-45)
* 0x 7e10 0034 PADS (GPIO 46-53)

Bits | Field Name | Description | Type | Reset
--- | --- | --- | --- | ---
31:24 | PASSWRD | Must be 5A when writing; Accidental write protect password | W | 0
23:5 | | **Reserved** - Write as 0, read as don't care | |
4 | SLEW | Slew rate; 0 = slew rate limited; 1 = slew rate not limited | RW | 0x1
3 | HYST | Enable input hysteresis; 0 = disabled; 1 = enabled | RW | 0x1
2:0 | DRIVE | Drive Strength, see breakdown list below | RW | 0x3

Beware of SSO (Simultaneous Switching Outputs) limitations which are not only device dependant but also depends on the quality and the layout of the PCB, amount and quality of the decoupling capacitors, type of load on the pads (resistance, capacitance) and other factors beyond control of Raspberry Pi.

#### Drive Strength list

  * 0 = 2mA
  * 1 = 4mA
  * 2 = 6mA
  * 3 = 8mA
  * 4 = 10mA
  * 5 = 12mA
  * 6 = 14mA
  * 7 = 16mA
