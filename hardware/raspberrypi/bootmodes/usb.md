# USB boot modes

There are two separate boot modes for USB:

* [USB device boot](/hardware/raspberrypi/bootmodes/device.md)
* [USB host boot](/hardware/raspberrypi/bootmodes/host.md) with boot options:
  * [USB mass storage boot](/hardware/raspberrypi/bootmodes/msd.md)
  * [Network boot](/hardware/raspberrypi/bootmodes/net.md)

Note that network boot is only possible on Raspberry Pi models that have a built-in wired Ethernet interface.

The choice between the two boot modes is made by the firmware at boot time when it reads the OTP bits. There are two bits to control USB boot: the first enables device boot and is enabled by default on all Raspberry Pi computers. The second bit enables USB host boot; if this bit is also set, then the processor reads the OTGID pin to decide whether to boot as a host (driven to zero as on the Raspberry Pi Model B) or as a device (left floating). The Pi Zero has access to this pin through the OTGID pin on the USB connector, and the Compute Module has access to this pin on the edge connector.

There are also OTP bits that allow certain GPIO pins to be used for selecting which boot modes the Pi should attempt to use.
