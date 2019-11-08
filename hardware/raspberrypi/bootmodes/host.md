# USB host boot mode

**USB host boot is available on Raspberry Pi 3B, 3B+, 3A+, and 2B v1.2 only. Raspberry Pi 3A+ only supports mass storage boot, not network boot.**

The USB host boot mode follows this sequence:

* Enable the USB port and wait for D+ line to be pulled high indicating a USB 2.0 device (we only support USB2.0)
* If the device is a hub:
    * Enable power to all downstream ports of the hub
    * For each port, loop for a maximum of two seconds (or five seconds if `program_usb_boot_timeout=1` has been set)
        * Release from reset and wait for D+ to be driven high to indicate that a device is connected
        * If a device is detected:
            * Send "Get Device Descriptor"
                * If VID == SMSC && PID == 9500
                    * Add device to Ethernet device list
            * If class interface == mass storage class
                * Add device to mass storage device list
* Else
    * Enumerate single device
* Go through mass storage device list
    * [Boot from mass storage device](msd.md)
* Go through Ethernet device list
    * [Boot from Ethernet](net.md)

