# Attaching a Raspberry Pi Camera Module to the Compute Module IO Board

## Notes before starting

These instructions are intended for expert users, if anything is unclear please use the [Raspberry Pi Camera forums](https://www.raspberrypi.org/forums/viewforum.php?f=43) for technical help. 

Unless explicitly stated otherwise, these instructions will work identically on both the Compute Module and Compute Module 3, attached to a Compute Module IO Board.

### Compute Module board capabilities

The Compute Module has two CSI-2 camera interfaces. CAM0 is a two lane interface, CAM1 is a four lane interface. The Compute Module IO board exposes both of these interfaces,  note that the standard Raspberry Pi devices uses CAM1, but only exposes two lanes.

### Updating your system

The camera software is under constant development. Please ensure your system is up to date prior to using these instructions.

```
sudo apt update
sudp apt full-upgrade
```

### Crypto Chip

When using the Compute Module to drive cameras, it is NOT necessary to incorporate the crypto chip used on the Raspberry Pi–designed camera boards when attaching the OM5647, IMX219 or HQ Camera Modules directly to the Compute Module carrier board. The Raspberry Pi firmware will automatically detect the CM and allow communications with the Camera Module to proceed without the crypto chip being present.


## Quickstart

1. On the compute module, run `sudo raspi-config` and enable the camera.
1. Next, run `sudo wget http://goo.gl/U4t12b -O /boot/dt-blob.bin`
1. Connect the RPI-CAMERA board and Camera Module to the CAM1 port. As an alternative, the Pi Zero camera cable can be used.

    ![Connecting the adapter board](images/CMAIO-Cam-Adapter.jpg)

1. Connect GPIO pins together as shown below.

    ![GPIO connection for a single camera](images/CMIO-Cam-GPIO.jpg)

1. (Optional) To add an additional camera, repeat step 3 with CAM0 and connect the GPIO pins for the second camera.

    ![GPIO connection with additional camera](images/CMIO-Cam-GPIO2.jpg)

1. Finally, reboot for the dt-blob.bin file to be read.

### Software support

The supplied camera applications `raspivid` and `raspistill` have the -cs (--camselect) option to specify which camera should be used.

If you are writing your own camera application based on the MMAL API you can use the MMAL_PARAMETER_CAMERA_NUM parameter to set the current camera. E.g.

```
MMAL_PARAMETER_INT32_T camera_num = {{MMAL_PARAMETER_CAMERA_NUM, sizeof(camera_num)}, CAMERA_NUMBER};
status = mmal_port_parameter_set(camera->control, &camera_num.hdr);
```

## Advanced

The Compute Module IO board has a 22-way 0.5mm FFC for each camera port, with CAM0 being a two-lane interface and CAM1 being the full four-lane interface. The standard Raspberry Pi uses a 15-way 1mm FFC cable, so you will need either an adapter (part# RPI-CAMERA) or a Pi Zero camera cable.

On the Compute Module IO board it is necessary to bridge the GPIOs and I2C interface required by the Raspberry Pi OS to the CAM1 connector. This is done by connecting the GPIOs from the J6 GPIO connector to the CD1_SDA/SCL and CAM1_IO0/1 pins on the J5 connector using jumper wires. Additionally, a `dt-blob.bin` file needs to be provided to override default pin states (the dt-blob.bin file is a file that tells the GPU what pins to use when controlling the camera. For more information on this, see the relevant section in the guide to attaching peripherals to a Compute Module [here](cm-peri-sw-guide.md)).

*The pin numbers below are provided only as an example. LED and SHUTDOWN pins can be shared by both cameras, if required.* The SDA and SCL pins must be either GPIO0 and GPIO1 or GPIO28 and 29 and must be individual to each camera.

### Steps to attach a Raspberry Pi Camera (to CAM1)

1. Attach the 0.5mm 22W FFC flexi (included with the RPI-CAMERA board) to the CAM1 connector (flex contacts face down). As an alternative, the Pi Zero camera cable can be used.
1. Attach the RPI-CAMERA adaptor board to the other end of the 0.5mm flex (flex contacts face down).
1. Attach a Raspberry Pi Camera to the other, larger 15W 1mm FFC on the RPI-CAMERA adaptor board (**contacts on the Raspberry Pi Camera flex must face up**).
1. Attach CD1_SDA (J6 pin 37) to GPIO0 (J5 pin 1).
1. Attach CD1_SCL (J6 pin 39) to GPIO1 (J5 pin 3).
1. Attach CAM1_IO1 (J6 pin 41) to GPIO2 (J5 pin 5).
1. Attach CAM1_IO0 (J6 pin 43) to GPIO3 (J5 pin 7).

Note, the numbers in brackets are conventional, physical pin numbers, numbered from left to right, top to bottom. The numbers on the silkscreen correspond to the Broadcom SoC GPIO numbers.

### Configuring default pin states

The GPIOs that we are using for the camera default to input mode on the Compute Module. To [override these default settings](../../configuration/pin-configuration.md) and also tell the system that these are the pins to be used by the camera, we need to create a `dt-blob.bin` that is loaded by the firmware when the system boots up. This file is built from a source dts file that contains the requried settings, and placed on the boot partition.

Some [Sample device tree source files](#sample-device-tree-source-files) are provided at the bottom of this document.

The `pin_config` section in the `pins_cm { }` (compute module) or `pins_cm3 { }` (compute module3) section of the source dts needs the camera's LED and power enable pins set to outputs:

```
pin@p2  { function = "output"; termination = "no_pulling"; };
pin@p3  { function = "output"; termination = "no_pulling"; };
```

To tell the firmware which pins to use and how many cameras to look for, add the following to the `pin_defines` section:

```
pin_define@CAMERA_0_LED { type = "internal"; number = <2>; };
pin_define@CAMERA_0_SHUTDOWN { type = "internal"; number = <3>; };
pin_define@CAMERA_0_UNICAM_PORT { type = "internal"; number = <1>; };
pin_define@CAMERA_0_I2C_PORT { type = "internal"; number = <0>; };
pin_define@CAMERA_0_SDA_PIN { type = "internal"; number = <0>; };
pin_define@CAMERA_0_SCL_PIN { type = "internal"; number = <1>; };
```

### How to attach two cameras

Attach the second camera to the (CAM0) connector as before.

Connect up the I2C and GPIO lines.

1. Attach CD0_SDA (J6 pin 45) to GPIO28 (J6 pin 1).
1. Attach CD0_SCL (J6 pin 47) to GPIO29 (J6 pin 3).
1. Attach CAM0_IO1 (J6 pin 49) to GPIO30 (J6 pin 5).
1. Attach CAM0_IO0 (J6 pin 51) to GPIO31 (J6 pin 7).

The Compute Module's **pin_config** section needs the second camera's LED and power enable pins configured:

```
pin@p30 { function = "output"; termination = "no_pulling"; };
pin@p31 { function = "output"; termination = "no_pulling"; };
```

In the Compute Module's **pin_defines** section of the dts file, change the **NUM_CAMERAS** parameter to 2 and add the following:

```
pin_define@CAMERA_1_LED { type = "internal"; number = <30>; };
pin_define@CAMERA_1_SHUTDOWN { type = "internal"; number = <31>; };
pin_define@CAMERA_1_UNICAM_PORT { type = "internal"; number = <0>; };
pin_define@CAMERA_1_I2C_PORT { type = "internal"; number = <0>; };
pin_define@CAMERA_1_SDA_PIN { type = "internal"; number = <28>; };
pin_define@CAMERA_1_SCL_PIN { type = "internal"; number = <29>; };
```

<a name="sample-device-tree-source-files"></a>
### Sample device tree source files

[Enable CAM1 only](dt-blob-cam1.dts)

[Enable both cameras](dt-blob-dualcam.dts)

### Compiling a DTS file to a device tree blob

Once all the required changes have been made to the `dts` file, it needs to be compiled and placed on the boot partition of the device. 

Instructions for doing this can be found on the [Pin Configuration](../../configuration/pin-configuration.md) page.
