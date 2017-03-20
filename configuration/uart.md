# The Raspberry Pi UARTS

The SoC's used on the Raspberry Pi's have two built in UARTS. On Raspberry Pi's equipped with the Wireless/Bluetooth module, one of those UARTS is used for communications with the module. The one used changed between the Raspberry Pi 3 and the Raspberry Pi Zero W. 

The two UARTS have slightly different characteristcs. They are both 3v3 devices, which means etra care must be taken when connecting up to an RS232 system. An adapter must be used to convert the voltage levels between the two protocols. Alterntaively, 3v3 USB UART adapters can be purchaed for very low prices. 

One UART is used for the Linux console, 

Linux ports vs Pi model

| Pi Model | Linux Device | Destination |
| - | - | - |
| 1,2 | /dev/


: ttyAMA0 now refers to the serial port that is connected to the bluetooth. The old serial port is now called ttyS0.
