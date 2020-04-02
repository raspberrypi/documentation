# Power Supply

The power supply requirements differ with Raspberry Pi model. All models require a 5.1v supply, but the current supplied generally increases according to model. All models up to the Raspberry Pi 3 require a microUSB power connector, whilst the Raspberry Pi 4 uses a USB-C connector.

Exactly how much current (mA) the Raspberry Pi requires is dependent on what you connect to it. The following table gives minimum and typical current requirements. 

| Product | Recommended PSU current capacity | Maximum total USB peripheral current draw | Typical bare-board active current consumption |
|-|-|-|-|
|Raspberry Pi Model A | 700mA | 500mA | 200mA |
| Raspberry Pi Model B |1.2A | 500mA | 500mA |
| Raspberry Pi Model A+ | 700mA | 500mA | 180mA
| Raspberry Pi Model B+ | 1.8A | 600mA/1.2A (switchable)| 330mA |
| Raspberry Pi 2 Model B | 1.8A | 600mA/1.2A (switchable) | 350mA |
| Raspberry Pi 3 Model B | 2.5A | 1.2A | 400mA |
| Raspberry Pi 3 Model A+ | 2.5A | Limited by PSU, board, and connector ratings only. | 350mA |
| Raspberry Pi 3 Model B+ | 2.5A | 1.2A | 500mA |
| Raspberry Pi 4 Model B | 3.0A | 1.2A | 600mA |
| Raspberry Pi Zero W/WH | 1.2A | Limited by PSU, board, and connector ratings only.| 150mA |
| Raspberry Pi Zero | 1.2A | Limited by PSU, board, and connector ratings only | 100mA |

Raspberry Pi have developed their own power supplies for use with all models. These are reliable, use heavy gauge wires and are reasonably priced. 

For Raspberry Pi 0-3, we recommend our [micro USB Supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/). For Raspberry Pi 4, we recommend our [USB-C Supply](https://www.raspberrypi.org/products/type-c-power-supply/)

The power requirements of the Raspberry Pi increase as you make use of the various interfaces on the Raspberry Pi. The GPIO pins can draw 50mA safely, distributed across all the pins; an individual GPIO pin can only safely draw 16mA. The HDMI port uses 50mA, the camera module requires 250mA, and keyboards and mice can take as little as 100mA or over 1000mA! Check the power rating of the devices you plan to connect to the Pi and purchase a power supply accordingly.

If you need to connect a USB device that will take the power requirements above the values specified in the table above, then you must connect it to an externally-powered USB hub.

## Backpowering

Backpowering occurs when USB hubs do not provide a diode to stop the hub from powering against the host computer. Other hubs will provide as much power as you want out each port. Please also be aware that some hubs will backfeed the Raspberry Pi. This means that the hubs will power the Raspberry Pi through its USB cable input cable, without the need for a separate micro-USB power cable, and bypass the voltage protection. If you are using a hub that backfeeds to the Raspberry Pi and the hub experiences a power surge, your Raspberry Pi could potentially be damaged.
