# Camera Modules

Raspberry Pi currently sell two types of camera board, an 8MP device and a 12MP HQ camera. The original 5MP device is no longer available from Raspberry Pi. The specifications of all the devices can be found [here](../../hardware/camera/README.md)


All modules are capable of taking full HD 1080p photo and video and can be controlled programmatically. This section of documentation describes how to use the camera in various scenarios, and using the various tools available.

For installation information, please see [this page](./installing.md)


## Basic camera usage

Once installed, there are various ways the cameras can be used. The simplest option is to use one of the provided camera applications. There are four Linux command line applications installed by default (e.g. raspistill), using these is described on [this page](raspicam/README.md).

You can also programatically access the camera using the [Python programming language](python/README.md).


## More advanced camera usage

The pages above describe some very basic ways of using the cameras, but they are very sophisticated devices that have some more advanced features.

Some of these features, along with some hints and tips, are described in the following pages.

- [Using RAW](./raspicam/raw.md)
- [Long exposures](./raspicam/longexp.md)
- [Directly accessing sensors](./raspicam/direct.md)
- [Using V4L2 to access the camera (e.g. Using Pi cameras as webcams)](./raspicam/v4l2.md)
- [Removing the HQ camera IR filter](../../hardware/camera/hqcam_filter_removal.md)

## libcamera - The future of Raspberry Pi camera software

libcamera is a new Linux API for interfacing to cameras. Raspberry Pi have been involved with the development of libcamera and are now using this sophisticated system for new camera software. This means Raspberry Pi are moving away from the firmware based camera image processing pipeline (ISP) to a more open system.

 - [Libcamera's main website](http://libcamera.org/).
 - [Raspberry Pi libcamera implementation](../../linux/software/libcamera/README.md).
 - [Tuning guide for the Raspberry Pi cameras and libcamera](../../linux/software/libcamera/rpi_SOFT_libcamera_1p0.pdf)
- [Writing a kernel module to support a new camera or capture chip](../../linux/software/libcamera/csi-2-usage.md)




