# GPIO pads control

Extracted from BCM2835 full data sheet, from Gert van Loo 2-August-2012.

### Address

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

Beware of SSO (Simultaneous Switching Outputs) limitations which are not only device dependant but also depends on the quality and the layout of the PCB, amount and quality of the decoupling capacitors, type of load on the pads (resistance, capacitance) and other factors beyond control of Broadcom.

#### Drive Strength list

  * 0 = 2mA
  * 1 = 4mA
  * 2 = 6mA
  * 3 = 8mA
  * 4 = 10mA
  * 5 = 12mA
  * 6 = 14mA
  * 7 = 16mA

#### How much current can the GPIO pins deliver?

There have been many questions about this on the Raspberry-Pi website. Also the fact that the above lists the drive strength in current made some user believe that the pads are somehow current limited.

That is **not** the case.

It may be easier to understand the behaviour if you know how the drive strength is controlled.
 
Inside the pad there is a whole bundle of drivers all in parallel. If the drive strength is set low(000) most of these are tri-stated so they do not add anything to the output current. If the drive strength is increased, more and more drivers are put in parallel. The following diagram shows that behaviour:

![GPIO Drive Strength Diagram](./images/pi_gpio_drive_strength_diagram.png)

#### What does the current value mean?

*The current value specifies the maximum current under which the pad will
still meet the specification*.

1. It is **not**: the current that the pad will deliver.
1. It is **not**: a current limit so the pad will not blow up.

The pad output is a voltage source:

* if set high the pad will try to drive the output to the rail voltage which on the Raspberry-Pi is 3V3 (3.3 Volts)
* if set low the pad will try to drive the output to ground (0 Volts)

As the text says: the pad will try to drive the output high or low. If it succeeds depends on what is connected. If the pas is shorted to ground it will not be able to drive high. In fact itwill try to deliver as much current as it can and the current is only limited to what the internal resistance is.

If you drive the pad high and it is shorted to ground in due time it will blow up! The same holds true if you connect it to 3V3 and drive it low.

Now I come back to the definition above:

The current value specifies the maximum current under which the pad will still meet the specification.

This has to do with the voltage levels guaranteed. As this is a digital pad there are two voltage levels: high and low. Yet how high and how low? Is high 0.9V or 1.5V or 2.7V or what?

To answer that question I/O ports have two parameters which deal with the output level:
*  V<sub>IL</sub>: The maximum low level voltage. (0.8V on the BCM2835)
*  V<sub>IH</sub> : The minimum high level voltage. (1.3V on the BCM2835)

V<sub>IL</sub>=0.8V means that if the output is Low it will be <= 0.8V.

V<sub>IL</sub>=1.3V means that if the output is High it will be >= 1.3V.
   
Thus a drive strength of 16mA means:

If you set the pad high you can draw up to 16mA and we still guarantee that the output voltage will be >=1.3V. This also means that if you set a drive strength of 2mA and you draw 16mA the voltage will **not** be 1.3 Volt but lower. In fact it may not be high enough to be seen as high by an external device.

#### Why don't I set all my pads to the maximum current?

Two reasons:

1. The raspberry-Pi 3V3 supply was designed with a maximum current of ~3mA per GPIO pin. If you load each pin with 16mA the total current is 272mA. The 3V3 supply will collapse under that!
1. Big current spikes will happen especially if you have a capacitive load. That will "bounce" around all the other pins near it. It is likely to cause interference with the SD-card or even the SDRAM behaviour.

#### What is a safe current?

All the electronics of the pads are designed for 16mA. That is a safe value under which youwill not damage the device. Even if you set the drive strength to 2mA and then load it so 16mA comes out that will not damage the device. Other than that there is no guaranteed maximum safe current.
