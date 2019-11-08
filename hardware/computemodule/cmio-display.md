# Attaching Raspberry Pi Official 7" Display to the Compute Module IO Board

**This document is a work in progress and is intended for advanced users.**

For the display to work with the Compute Module, the firmware needs to be from October 23rd 2015 or later (use `vcgencmd version` to check). For the display to work with the Compute Module 3, the firmware needs to be from October 2016 or later.

**Note:** The Raspberry Pi Zero camera cable cannot be used as an alternative to the RPI-DISPLAY adaptor, because its wiring is different.   

## Quickstart — display only

1. Connect the display to the DISP1 port on the Compute Module IO board through the 22W to 15W display adaptor.
1. Connect these pins together with jumper wires:

	```
	GPIO0 - CD1_SDA
	GPIO1 - CD1_SCL
	```

1. On the Compute Module, run:

	```sudo wget https://goo.gl/iiVxuA -O /boot/dt-blob.bin```

1. Reboot for the `dt-blob.bin` file to be read.

## Quickstart — display and camera(s)
This will enable `disp1` and `cam1`, with the option of enabling `cam0`.

1. Connect the display to the DISP1 port on the Compute Module IO board through the 22W to 15W display adaptor, called RPI-DISPLAY.
1. Connect the Camera Module to the CAM1 port on the Compute Module IO board through the 22W to 15W adaptor called RPI-CAMERA. Alternatively, the Raspberry Pi Zero camera cable can be used.
1. (Optional) Connect the Camera Module to the CAM0 port on the Compute Module IO board through the 22W to 15W adaptor called RPI-CAMERA. Alternatively, the Raspberry Pi Zero camera cable can be used.
1. Connect these pins together with jumper wires:

	```
	GPIO0 - CD1_SDA
	GPIO1 - CD1_SCL
	GPIO4 - CAM1_IO1
	GPIO5 - CAM1_IO0
	```
Please note that the wiring is slightly different from that on the Camera page, in that you are using GPIO pins 4 and 5 instead of 2 and 3.

1. For `cam0`, add links:

	```
	GPIO28 - CD0_SDA
	GPIO29 - CD0_SCL
	GPIO30 - CAM0_IO1
	GPIO31 - CAM0_IO0
	```

	![GPIO connection for a single display and two Camera Modules](images/CMIO-Cam-Disp-GPIO.jpg)
	(Please note this image needs to be updated to show two Camera Modules, or have the extra jumper leads removed)

1. On the Compute Module, for the display and one Camera Module, run:

	```sudo wget https://goo.gl/gaqNrO -O /boot/dt-blob.bin```  

  For the display and two Camera Modules, run:

	```sudo wget https://goo.gl/htHv7m -O /boot/dt-blob.bin```

1. Reboot for the `dt-blob.bin` file to be read.

	![Camera Preview on the 7 inch display](images/CMIO-Cam-Disp-Example.jpg)
	(Please note this image needs to be updated to show two Camera Modules, or have the extra jumper leads removed)

### Software support

There is no additional configuration required to enable the touchscreen. The touch interface should out work of the box once the screen is successfully detected.


### Sources
- [dt-blob-disp1-only.dts](dt-blob-disp1-only.dts)
- [dt-blob-disp1-cam1.dts](dt-blob-disp1-cam1.dts)
- [dt-blob-disp1-cam2.dts](dt-blob-disp1-cam2.dts)
