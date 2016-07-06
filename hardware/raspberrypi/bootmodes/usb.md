# USB boot modes

There are two separate boot modes for USB the device and the host boot modes.  The device boot mode and the host boot mode, the choice
between the two modes is done at boot time by reading the OTP bits, there are two bits to control USB boot, the first enables device boot
and is enabled by default on all Raspberry Pi devices.  The second bit enables USB host boot, if this bit is also set then the processor
reads the OTGID pin to device whether to boot as a host (driven to zero as on the Pi Model B) or as a device (left floating).  The
Pi Zero has access to this pin through the OTGID pin on the USB connector, the compute module has access to this pin on the edge connector.

* [USB host boot](host.md)
* [USB device boot](device.md)
