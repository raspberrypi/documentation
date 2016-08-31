# USB Host boot mode

The USB host boot mode follows this sequence:

* Enable the USB port and wait for D+ line to be pulled high indicating a USB 2.0 device (we only support USB2.0)
* If the device is a hub:
  * Enable power to all downstream ports of the hub
  * For each port loop for a maximum of 2 seconds (or 5 seconds  if `program_usb_timeout=1` has been set)
    * Release from reset and wait for D+ to be driven high to indicate a device is connected
    * If device detected
      * Send "Get Device Descriptor"
        * If VID == SMSC && PID == 9500
          * Add device to ethernet device list
        * If class interface == mass storage class
          * Add device to MSD device list
* else
  * Just enumerate single device
* Go through MSD device list
  * [Boot from MSD](msd.md)
* Go through Ethernet device list
  * [Boot from Ethernet](net.md)

