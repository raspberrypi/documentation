# Power Supply

The power supply requirements differ by Raspberry Pi model. All models require a 5.1V supply, but the current supplied generally increases according to model. All models up to the Raspberry Pi 3 require a microUSB power connector, whilst the Raspberry Pi 4 uses a USB-C connector.

Exactly how much current (mA) the Raspberry Pi requires is dependent on what you connect to it. The following table gives various current requirements. 

| Product | Recommended PSU current capacity | Maximum total USB peripheral current draw | Typical bare-board active current consumption |
|-|-|-|-|
|Raspberry Pi Model A | 700mA | 500mA | 200mA |
| Raspberry Pi Model B |1.2A | 500mA | 500mA |
| Raspberry Pi Model A+ | 700mA | 500mA | 180mA
| Raspberry Pi Model B+ | 1.8A | 1.2A | 330mA |
| Raspberry Pi 2 Model B | 1.8A | 1.2A | 350mA |
| Raspberry Pi 3 Model B | 2.5A | 1.2A | 400mA |
| Raspberry Pi 3 Model A+ | 2.5A | Limited by PSU, board, and connector ratings only. | 350mA |
| Raspberry Pi 3 Model B+ | 2.5A | 1.2A | 500mA |
| Raspberry Pi 4 Model B | 3.0A | 1.2A | 600mA |
| Raspberry Pi Zero | 1.2A | Limited by PSU, board, and connector ratings only | 100mA |
| Raspberry Pi Zero W/WH | 1.2A | Limited by PSU, board, and connector ratings only.| 150mA |

Raspberry Pi have developed their own power supplies for use with all models. These are reliable, use heavy gauge wires and are reasonably priced. 

For Raspberry Pi 0-3, we recommend our [2.5A micro USB Supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/). For Raspberry Pi 4, we recommend our [3A USB-C Supply](https://www.raspberrypi.org/products/type-c-power-supply/)

The power requirements of the Raspberry Pi increase as you make use of the various interfaces on the Raspberry Pi. The GPIO pins can draw 50mA safely, distributed across all the pins; an individual GPIO pin can only safely draw 16mA. The HDMI port uses 50mA, the camera module requires 250mA, and keyboards and mice can take as little as 100mA or over 1000mA! Check the power rating of the devices you plan to connect to the Pi and purchase a power supply accordingly.

If you need to connect a USB device that will take the power requirements above the values specified in the table above, then you must connect it to an externally-powered USB hub.

## Power Supply Warnings

On all models of Raspberry Pi since the Raspberry Pi B+ (2014) except the Zero range, there is low-voltage detection circuitry that will detect if the supply voltage drops below 4.63V (+/- 5%). This will result in a [warning icon](../../../configuration/warning-icons.md) being displayed on all attached displays and an entry being added to the kernel log.

If you are seeing warnings, you should improve the power supply and/or cable, as low power can cause problems with corruption of SD cards, or erratic behaviour of the Pi itself; for example, unexplained crashes. 

Voltages can drop for a variety of reasons, for example if the power supply itself is inadequate, the power supply cable is made of too thin wires, or you have plugged in high demand USB devices. 

## Backpowering

Backpowering occurs when USB hubs do not provide a diode to stop the hub from powering against the host computer. Other hubs will provide as much power as you want out each port. Please also be aware that some hubs will backfeed the Raspberry Pi. This means that the hubs will power the Raspberry Pi through its USB cable input cable, without the need for a separate micro-USB power cable, and bypass the voltage protection. If you are using a hub that backfeeds to the Raspberry Pi and the hub experiences a power surge, your Raspberry Pi could potentially be damaged.
