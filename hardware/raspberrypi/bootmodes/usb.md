# USB boot modes

There are two separate boot modes for USB: 

* [USB device boot](device.md)
* [USB host boot](host.md) with boot options:
  * [USB Mass storage boot](msd.md)
  * [Network boot](net.md)

Note that network boot is only possible from the wired ethernet interfaces built into certain models of Raspberry Pi.

The choice between the two boot modes is made at boot time by the firmware by reading the OTP bits. There are two bits to control USB boot: the first enables device boot and is enabled by default on all Raspberry Pi devices. The second bit enables USB host boot; if this bit is also set then the processor reads the OTGID pin to decide whether to boot as a host (driven to zero as on the Raspberry Pi Model B) or as a device (left floating). The Pi Zero has access to this pin through the OTGID pin on the USB connector, and the compute module has access to this pin on the edge connector.

There are also OTP bits to allow certain GPIO pins to be used to select which boot modes the Pi should attempt to use.
