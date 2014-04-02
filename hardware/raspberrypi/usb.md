# USB

USB on the Raspberry Pi

## Overview

The Raspberry Pi Model B is equipped with two USB2.0 ports. These are connected to the LAN9512 combo hub/Ethernet chip IC3, which is itself a USB device connected to BCM2835.

On the Model A, the single USB2.0 port is directly wired to BCM2835.

The USB host inside BCM2835 is an On-The-Go (OTG) host as BCM2835 was originally intended to be used in the mobile market: i.e. as the single USB port on a phone for connection to a PC, or to a single device.

OTG in general supports all types of USB devices, but does so by providing a simpler level of autonomous support than a PC host does in order to keep costs low. To provide an adequate level of functionality for most of the USB devices that one might plug into a Pi, the system driver has to perform more processing in software.

## Port Power

USB2.0 devices have defined power requirements, in units of 100mA from 100mA to 500mA. The device advertises its own power requirements to the USB host when it is first connected.

The USB ports on a Raspberry Pi have a design loading of 100mA - sufficient to drive "low-power" devices such as mice and keyboards. Devices such as Wi-Fi adapters, USB hard drives, USB pen drives all consume much more current and should be powered from an external hub with its own power supply. While it is possible to plug a 500mA device into a Pi and have it work with a sufficiently powerful supply, reliable operation is not guaranteed.

In addition, hotplugging high-power devices into the Pi's USB ports may cause a brownout which can cause the Pi to reset.

See [Power](power.md) for more information.

## Supported devices

In general, every device supported by Linux is possible to use with the Pi. Linux has probably the most comprehensive driver database for legacy hardware of any operating system (it can lag behind for modern device support as it requires open-source drivers for Linux to recognise the device by default).

If you have a device and wish to use it with a Pi, then plug it in. Chances are that it'll "just work".

If a device doesn't work, then the first step is to see if it is detected at all. There are two commands that can be entered into a terminal for this: lsusb and dmesg. The first will print out all devices attached to USB, whether they are actually recognised or not, and the second will print out the kernel message buffer (which can be quite big after booting - try doing sudo dmesg -C then plug in your device and retype dmesg to see new messages).

As an example with a USB pendrive:
```
pi@raspberrypi ~ $ lsusb
Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp.
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.
Bus 001 Device 005: ID 05dc:a781 Lexar Media, Inc.
pi@raspberrypi ~ $ dmesg
... Stuff that happened before ...
[ 8904.228539] usb 1-1.3: new high-speed USB device number 5 using dwc_otg
[ 8904.332308] usb 1-1.3: New USB device found, idVendor=05dc, idProduct=a781
[ 8904.332347] usb 1-1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[ 8904.332368] usb 1-1.3: Product: JD Firefly
[ 8904.332386] usb 1-1.3: Manufacturer: Lexar
[ 8904.332403] usb 1-1.3: SerialNumber: AACU6B4JZVH31337
[ 8904.336583] usb-storage 1-1.3:1.0: USB Mass Storage device detected
[ 8904.337483] scsi1 : usb-storage 1-1.3:1.0
[ 8908.114261] scsi 1:0:0:0: Direct-Access     Lexar    JD Firefly       0100 PQ: 0 ANSI: 0 CCS
[ 8908.185048] sd 1:0:0:0: [sda] 4048896 512-byte logical blocks: (2.07 GB/1.93 GiB)
[ 8908.186152] sd 1:0:0:0: [sda] Write Protect is off
[ 8908.186194] sd 1:0:0:0: [sda] Mode Sense: 43 00 00 00
[ 8908.187274] sd 1:0:0:0: [sda] No Caching mode page present
[ 8908.187312] sd 1:0:0:0: [sda] Assuming drive cache: write through
[ 8908.205534] sd 1:0:0:0: [sda] No Caching mode page present
[ 8908.205577] sd 1:0:0:0: [sda] Assuming drive cache: write through
[ 8908.207226]  sda: sda1
[ 8908.213652] sd 1:0:0:0: [sda] No Caching mode page present
[ 8908.213697] sd 1:0:0:0: [sda] Assuming drive cache: write through
[ 8908.213724] sd 1:0:0:0: [sda] Attached SCSI removable disk
```

In this case, there are no error messages in dmesg and the pendrive is detected by usb-storage. If your device did not have a driver available, then typically only the first 6 new lines will appear in the dmesg printout.

If a device enumerates without any errors, but doesn't appear to do anything, then it is likely there are no drivers installed for it. Search around, based on the manufacturer's name for the device or the USB IDs that are displayed in lsusb (e.g. 05dc:a781). The device may not be supported with default Linux drivers - and you may need to download or compile your own third-party software.

##Hubs

In the USB2.0 specification, there is a large section dedicated to how a USB hub must be implemented and the behaviours that it must perform, for example, when devices are plugged in that exceed its own upstream power capabilities. In addition, there are two implementation choices available to hub chip manufacturers: these alter the behaviour when talking to low- or full-speed (USB1.1) devices plugged into a USB2.0 hub.

Not all hubs are created equal.

### Transaction Translators (TTs)

USB2.0 defines three bus speeds: Low (1.5mbps), Full (12mbps) and High (480mbps). The choice of speed class for a device is a function of how much bandwidth the device requires, the cost when designing the chip and cost when designing the circuit board inside the device.

Keyboards and mice are classically Low-speed devices, as the bandwidth requirement is of the order of bytes per second. Audio and bluetooth devices are typically Full-speed and most video devices (excluding the cheapest) are High-speed.

To talk to a Low- or Full-speed device on a High speed bus, a hub must be used. Hubs contain at least one Transaction Translator (or TT) - a function of the hub chip that takes high-speed packets and buffers them for transmission at slow speed to the lower-speed device. Similarly, data from the lower-speed device the data is buffered and then transmitted in a faster burst to the host.

Hubs are allowed to implement either a Single TT (one TT for all ports, shared between them) or Multiple TT (one TT per port). Note that this definition is per hub *chip*, not per physical hub as we will see later.

### Hubs and the Pi

Because of certain hardware constraints within the USB OTG hardware on the Pi, the use of a Multi-TT hub is strongly recommended when using multiple full- or low-speed devices.

In the absence of a Multi-TT hub, spread devices out between hubs as much as possible. 

### Common deviations from the Hub Specification

1. Back-powering
   The USB specification states that no hub shall present power from the downstream external power source to the upstream port. Cheap hubs are terrible at complying with this requirement: the 5V is simply connected straight from upstream to the external power adapter.
2. No overcurrent protection or switching
   Hubs must protect against overcurrent conditions on downstream ports, either by switching off the port automatically or allowing a resettable polyfuse to blow. Many hubs have no such protections and just connect all downstream port power together.
3. Daisy-chained hubs
   A 7-port hub is rarely a 7-port hub. Cheaper versions of these will typically use two 4-port hub ICs and package them together to make a "7 port" variant. There is a limitation in the USB specification on how "deep" hubs can be daisy-chained: up to a maximum of 5 hubs between the host and the device.
4. Broken hub descriptors
   Hubs have implementation-specific descriptors that should detail how many ports are available, whether port power switching is ganged or single-port and how much total bus current the hub can supply. Certain broken hubs have bogus information in these descriptors: claiming to be only able to supply 2mA or other nonsense. Linux will comply with the standard and refuse to enumerate devices without enough power available.
