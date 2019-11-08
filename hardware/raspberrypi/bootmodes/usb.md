# USB boot modes

There are two separate boot modes for USB (available only on certain models): 

* [USB device boot](device.md)
* [USB host boot](host.md) with boot options:
  * [USB mass storage boot](msd.md)
  * [Network boot](net.md)

The choice between the two boot modes is made by the firmware at boot time when it reads the OTP bits. There are two bits to control USB boot: the first enables USB device boot and is enabled by default. The second enables USB host boot; if the USB host boot mode bit is set, then the processor reads the OTGID pin to decide whether to boot as a host (driven to zero as on the Raspberry Pi Model B) or as a device (left floating). The Pi Zero has access to this pin through the OTGID pin on the USB connector, and the Compute Module has access to this pin on the edge connector.

There are also OTP bits that allow certain GPIO pins to be used for selecting which boot modes the Pi should attempt to use.
