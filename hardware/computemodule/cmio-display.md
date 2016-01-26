# Attaching Raspberry Pi Official 7 inch Display to the Compute Module IO Board

*This document is a work in progress and is intended for advanced users.*

For the display to work with the compute module, the firmware needs to be October 23rd 2015 or newer (use `vcgencmd version` to check).

## Quickstart - Display Only

1. Connect the display to the DISP1 port on the Compute Module IO Board through the 22W to 15W display adaptor.
1. Connect these pins together with jumper wires:

	```
	GPIO0 - CD1_SDA
	GPIO1 - CD1_SCL
	```

1. On the compute module, run:

	```sudo wget https://goo.gl/Ah6XD5 -O /boot/dt-blob.bin```

1. Reboot for the `dt-blob.bin` file to be read.

## Quickstart - Display and Camera
*This will enable `disp1` and `cam1`*

1. Connect the display to the DISP1 port on the Compute Module IO Board through the 22W to 15W display adaptor.
1. Connect the camera to the CAM1 port on the Compute Module IO Board through the 22W to 15W camera adaptor.
1. Connect these pins together with jumper wires:

	```
	GPIO0 - CD0_SDA
	GPIO1 - CD0_SCL
	GPIO4 - CAM0_IO1
	GPIO5 - CAM0_IO0

	GPIO28 - CD1_SDA
	GPIO29 - CD1_SCL
	GPIO30 - CAM1_IO1
	GPIO31 - CAM1_IO0
	```

	![GPIO connection for a single display and a single camera](images/CMIO-Cam-Disp-GPIO.jpg)

1. On the compute module, run:

	```sudo wget https://goo.gl/1V3ReK -O /boot/dt-blob.bin```

1. Make the 7 inch display as the default by adding the following line into `/boot/config.txt`:

	```
	display_default_lcd=1
	```
1. Reboot for the `dt-blob.bin` file to be read.

	![Camera Preview on the 7 inch display](images/CMIO-Cam-Disp-Example.jpg)

### Software support

There is no additional configuration required to enable the touch screen. The touch interface should out work of the box once the screen is successfully detected.


### Sources
- [dt-blob-disp1-cam1.dts](dt-blob-disp1-cam1.dts)
- [dt-blob-disp1-only.dts](dt-blob-disp1-only.dts)
