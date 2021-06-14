# USB

In general, every device supported by Linux can be used with a Raspberry Pi, although there are some limitations for models prior to Pi 4.

## Power

As with all computers, the USB ports on the Raspberry Pi supply a limited amount of power. Often problems with USB devices are caused by power issues. To rule out power as the cause of an problem, connect your USB devices to the Raspberry Pi using a powered hub.

| Model | Max power output of USB ports |
|-------|-------------------|
| Pi Zero, 1  | 500mA per port<sup>1</sup>    |
| Pi 2, 3, 4  | 1200mA total across all ports |

1. For the original Pi 1B the limit is 100mA per port.

## Raspberry Pi 4

The Pi 4 contains two USB 3.0 ports and two USB 2.0 ports which are connected to a VL805 USB controller. The USB 2.0 lines on all four ports are connected to a single USB 2.0 hub within the VL805: this limits the total available bandwidth for USB 1.1 and USB 2.0 devices to that of a single USB 2.0 port.

On the Pi 4, the USB controller used on previous models is located on the USB type C port and is disabled by default.

## Raspberry Pi Zero, 1, 2 and 3

The USB controller on models prior to Pi 4 has only a basic level of support for certain devices, which presents a higher software processing overhead. It also supports only one root USB port: all traffic from connected devices is funnelled down this single bus, which operates at a maximum speed of 480mbps.

The USB 2.0 specification defines three device speeds - low, full and high. Most mice and keyboards are low speed, most USB sound devices are full speed and most video devices (webcams or video capture) are high speed.

Generally, there are no issues with connecting multiple high speed USB devices to a Pi.

The software overhead incurred when talking to low and full speed devices means that there are limitations on the number of simultaneously active low and full speed devices. Small numbers of these types of devices connected to a Pi will cause no issues.

### Known issues

**1. Interoperability with USB 3.0 hubs**  
There is an issue with USB 3.0 hubs in conjunction with the use of full or low speed devices, including most mice and keyboards. A bug in most USB 3.0 hub hardware means that the models prior to Pi 4 cannot talk to full or low speed devices connected to a USB 3.0 hub.

USB 2.0 high speed devices, including USB 2.0 hubs, operate correctly when connected via a USB 3.0 hub.

Avoid connecting low or full speed devices into a USB 3.0 hub. As a workaround, plug a USB 2.0 hub into the downstream port of the USB 3.0 hub and connect the low speed device, or use a USB 2.0 hub between the Pi and the USB 3.0 hub, then plug low speed devices into the USB 2.0 hub.

**2. USB 1.1 webcams**  
Old webcams may be full speed devices. Because these devices transfer a lot of data and incur additional software overhead, reliable operation is not guaranteed. As a workaround, try to use the camera at a lower resolution.

**3. Esoteric USB sound cards**  
Expensive audiophile sound cards typically use large amounts of USB bandwidth: reliable operation with 96kHz/192kHz DACs is not guaranteed. As a workaround, forcing the output stream to be CD quality (44.1kHz/48kHz 16-bit) will reduce the stream bandwidth to reliable levels.

**4. Single TT USB hubs**  
USB 2.0 and 3.0 hubs have a mechanism for talking to full or low speed devices connected to their downstream ports called a transaction translator (TT). This device buffers high speed requests from the host and transmits them at full or low speed to the downstream device. Two configurations of hub are allowed by the USB specification: Single TT (one TT for all ports) and Multi TT (one TT per port). Because of a hardware limitation, if too many full or low speed devices are plugged into a single TT hub, the devices may behave unreliably. It is recommended to use a Multi TT hub to interface with multiple full and low speed devices. As a workaround, spread full and low speed devices out between the Pi's own USB port and the single TT hub.
