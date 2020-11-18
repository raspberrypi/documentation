# CSI-2 (Camera Serial Interface 2) "Unicam"

The SoC's used on the Raspberry Pi range all have two camera interfaces that support either CSI-2 D-PHY 1.1 or CCP2 (Compact Camera Port 2) sources. This interface is known by the codename "Unicam". The first instance of Unicam supports 2 CSI-2 data lanes, whilst the second supports 4. Each lane can run at up to 1Gbit/s (DDR, so the max link frequency is 500MHz).

However, the normal variants of the Raspberry Pi only expose the second instance, and route out *only* 2 of the data lanes to the camera connector. The Compute Module range route out all lanes from both peripherals.

## Software Interfaces 

There are 3 independent software interfaces available for communicating with the  Unicam peripheral:

### Firmware

The closed source GPU firmware has drivers for Unicam and three camera sensors plus a bridge chip. They are the Raspberry Pi Camera v1.3 (Omnivision OV5647), Raspberry Pi Camera v2.1 (Sony IMX219), Raspberry Pi HQ camera (Sony IMX477), and an unsupported driver for the Toshiba TC358743 HDMI->CSI2 bridge chip.

This driver integrates the source driver, Unicam, ISP, and tuner control into a full camera stack delivering processed output images. It can be used via MMAL, OpenMAX IL and V4L2 using the bcm2835-v4l2 kernel module. Only Raspberry Pi cameras are supported via this interface.

### MMAL rawcam component

This was an interim option before the V4L2 driver was available. The MMAL component `vc.ril.rawcam` allows receiving of the raw CSI2 data in the same way as the V4L2 driver, but all source configuration has to be done by userland over whatever interface the source requires. The raspiraw application is available on [github]( https://github.com/raspberrypi/raspiraw). It uses this component and the standard I2C register sets for OV5647, IMX219, and ADV7282M to support streaming.


### V4L2

There is a fully open source kernel driver available for the Unicam block; this is a kernel module called bcm2835-unicam. This interfaces to V4L2 subdevice drivers for the source to deliver the raw frames. This bcm2835-unicam driver controls the sensor, and configures the CSI-2 receiver so that the peripheral will write the raw frames (after Debayer) to SDRAM for V4L2 to deliver to applications. Except for this ability to unpack the CSI-2 Bayer formats to 16bits/pixel, there is no image processing between the image source (e.g. camera sensor) and bcm2835-unicam placing the image data in SDRAM.

```
|------------------------|
|     bcm2835-unicam     |
|------------------------|
     ^             |
     |      |-------------|
 img |      |  Subdevice  |
     |      |-------------|
     v   -SW/HW-   |
|---------|   |-----------|
| Unicam  |   | I2C or SPI|
|---------|   |-----------|
csi2/ ^             |
ccp2  |             |
    |-----------------|
    |     sensor      |
    |-----------------|
```

Mainline Linux has a range of existing drivers. The Raspberry Pi kernel tree has some additional drivers and device tree overlays to configure them that have all been tested and confirmed to work. They include:

| Device | Type | Notes |
| :----- | :--- | :---- |
| Omnivision OV5647 | 5MP Camera | Original Raspberry Pi Camera |
| Sony IMX219 | 8MP Camera | Revision 2 Raspberry Pi camera |
| Sony IMX477 | 12MP Camera | Raspberry Pi HQ camera |
| Toshiba TC358743 | HDMI to CSI-2 bridge | |
| Analog Devices ADV728x-M | Analog video to CSI-2 bridge| No interlaced support |
| Infineon IRS1125 | Time-of-flight depth sensor| Supported by a third party |

As the subdevice driver is also a kernel driver, with a standardised API, 3rd parties are free to write their own for any source of their choosing. 

## Developing a third-party driver for bcm2835-unicam

This is the recommended approach to interfacing via Unicam.

When developing a driver for a new device intended to be used with the bcm2835-unicam module, you need the driver and corresponding device tree overlays. Ideally the driver should be submitted to the [linux-media](http://vger.kernel.org/vger-lists.html#linux-media) mailing list for code review and merging into mainline, then moved to the [Raspberry Pi kernel tree](https://github.com/raspberrypi/linux), but exceptions may be made for the driver to be reviewed and merged directly to the Raspberry Pi kernel.

Please note that all kernel drivers are licensed under the GPLv2 licence, therefore source code **MUST** be available. Shipping of binary modules only is a violation of the GPLv2 licence under which the Linux kernel is licensed. 

The bcm2835-unicam has been written to try and accommodate all types of CSI-2 source driver as are currently found in the mainline Linux kernel. Broadly these can be split into camera sensors and bridge chips. Bridge chips allow for conversion between some other format and CSI-2.

### Camera sensors

The sensor driver for a camera sensor is responsible for all configuration of the device, usually via I2C or SPI. Rather than writing a driver from scratch, it is often easier to take an existing driver as a basis and modify it as appropriate. 

The IMX219 driver is a good starting point, the version found in the 5.4 kernel can be found [here](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/drivers/media/i2c/imx219.c). This driver supports both 8bit and 10bit Bayer readout, so enumerating frame formats and frame sizes is slightly more involved. 

Sensors generally support V4L2 user controls which are documented [here](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/control.html). Not all these controls need to be implemented in a driver. The IMX219 driver only implements a small subset, listed below, the implementation of which is handled by the `imx219_set_ctrl` function.

- `V4L2_CID_PIXEL_RATE` / `V4L2_CID_VBLANK` / `V4L2_CID_HBLANK`: allows the application to set the frame rate.
- `V4L2_CID_EXPOSURE`: sets the exposure time in lines. The application needs to use `V4L2_CID_PIXEL_RATE`, `V4L2_CID_HBLANK`, and the frame width to compute the line time.
- `V4L2_CID_ANALOGUE_GAIN`: analogue gain in sensor specific units.
- `V4L2_CID_DIGITAL_GAIN`: optional digital gain in sensor specific units.
- `V4L2_CID_HFLIP / V4L2_CID_VFLIP`: flips the image either horizontally or vertically. Note that this operation may change the Bayer order of the data in the frame, as is the case on the imx219.
- `V4L2_CID_TEST_PATTERN` / `V4L2_CID_TEST_PATTERN_*`: Enables output of various test patterns from the sensor. Useful for debugging.

In the case of the IMX219, many of these controls map directly onto register writes to the sensor itself.

Device tree is used to select the sensor driver and configure
parameters such as number of CSI-2 lanes, continuous clock lane
operation, and link frequency (often only one is supported). The IMX219 device tree overlay for the 5.4 kernel can be found [here](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/arch/arm/boot/dts/overlays/imx219-overlay.dts)

### Bridge chips

These are devices that convert an incoming video stream, for example HDMI or composite, into a CSI-2 stream that can be accepted by the Raspberry Pi CSI-2 receiver.

Handling bridge chips is more complicated, as unlike camera sensors they have to respond to the incoming signal and report that to the application.  

The mechanisms for handling bridge chips can be broadly split into either analogue or digital. 

When using `ioctls` in the sections below, an `_S_` in the `ioctl` name means it is a set function, whilst `_G_` is a get function and `_ENUM` enumerates a set of permitted values. 

#### Analogue video sources

Analogue video sources use the standard `ioctls` for detecting and setting video standards. :[`VIDIOC_G_STD`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-g-std.html), [`VIDIOC_S_STD`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-g-std.html), [`VIDIOC_ENUMSTD`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-enumstd.html), and [`VIDIOC_QUERYSTD`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-querystd.html)

 Selecting the wrong standard will generally result in corrupt images. Setting the standard will typically also set the resolution on the V4L2 CAPTURE queue. It can not be set via `VIDIOC_S_FMT`. Generally requesting the detected standard via `VIDIOC_QUERYSTD` and then setting it with `VIDIOC_S_STD` before streaming is a good idea. 

#### Digital video sources

For digital video sources, such as HDMI, there is an alternate set of calls that allow specifying of all the digital timing parameters ([`VIDIOC_G_DV_TIMINGS`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-g-dv-timings.html), [`VIDIOC_S_DV_TIMINGS`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-g-dv-timings.html), [`VIDIOC_ENUM_DV_TIMINGS`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-enum-dv-timings.html), and [`VIDIOC_QUERY_DV_TIMINGS`](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-query-dv-timings.html)). 

As with analogue bridges, the timings typically fix the V4L2 CAPTURE queue resolution, and calling `VIDIOC_S_DV_TIMINGS` with the result of `VIDIOC_QUERY_DV_TIMINGS` before streaming should ensure the format is correct.

Depending on the bridge chip and the driver, it may be possible for changes in the input source to be reported to the application via `VIDIOC_SUBSCRIBE_EVENT` and `V4L2_EVENT_SOURCE_CHANGE`.

#### Currently supported devices

There are 2 bridge chips that are currently supported by the Rasberry Pi Linux kernel, the Analog Devices ADV728x-M for analogue video sources, and the Toshiba TC358743 for HDMI sources. 


*Analog Devices ADV728x(A)-M Analogue video to CSI2 bridge*

These chips convert composite, S-video (Y/C), or component (YPrPb) video into a single lane CSI-2 interface, and are supported by the [ADV7180 kernel driver](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/drivers/media/i2c/adv7180.c).

Product details for the various versions of this chip can be found on the Analog Devices website. 

[ADV7280A](https://www.analog.com/en/products/adv7280a.html), [ADV7281A](https://www.analog.com/en/products/adv7281a.html), [ADV7282A](https://www.analog.com/en/products/adv7282a.html)

Because of some missing code in the current core V4L2 implementation, selecting the source fails, so the Raspberry Pi kernel version adds a kernel module parameter called `dbg_input` to the ADV7180 kernel driver which sets the input source every time VIDIOC_S_STD is called. At some point mainstream will fix the underlying issue (a disjoin between the kernel API call s_routing, and the userspace call `VIDIOC_S_INPUT`) and this modification will be removed.

Please note that receiving interlaced video is not supported, therefore the ADV7281(A)-M version of the chip is of limited use as it doesn't have the necessary I2P deinterlacing block. Also ensure when selecting a device to specify the -M option. Without that you will get a parallel output bus which can not be interfaced to the Raspberry Pi.

There are no known commercially available boards using these chips, but this driver has been tested via the Analog Devices [EVAL-ADV7282-M evaluation board](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/EVAL-ADV7282A-M.html)

This driver can be loaded using the `config.txt` dtoverlay `adv7282m` if you are using the `ADV7282-M` chip variant; or `adv728x-m` with a parameter of either `adv7280m=1`, `adv7281m=1`, or `adv7281ma=1` if you are using a different variant. e.g.
```
dtoverlay=adv728x-m,adv7280m=1
```

*Toshiba TC358743 HDMI to CSI2 bridge*

This is a HDMI to CSI-2 bridge chip, capable of converting video data at up to 1080p60.

Information on this bridge chip can be found on the [Toshiba Website](https://toshiba.semicon-storage.com/ap-en/semiconductor/product/interface-bridge-ics-for-mobile-peripheral-devices/hdmir-interface-bridge-ics/detail.TC358743XBG.html)

The TC358743 interfaces HDMI in to CSI-2 and I2S outputs. It is supported by the [TC358743 kernel module](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/drivers/media/i2c/tc358743.c).

The chip supports incoming HDMI signals as either RGB888, YUV444, or YUV422, at up to 1080p60. It can forward RGB888, or convert it to YUV444 or YUV422, and convert either way between YUV444 and YUV422. Only RGB888 and YUV422 support has been tested. When using 2 CSI-2 lanes, the maximum rates that can be supported are 1080p30 as RGB888, or 1080p50 as YUV422. When using 4 lanes on a Compute Module, 1080p60 can be received in either format.

HDMI negotiates the resolution by a receiving device advertising an [EDID](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data) of all the modes that it can support. The kernel driver has no knowledge of the resolutions, frame rates, or formats that you wish to receive, therefore it is up to the user to provide a suitable file.
This is done via the VIDIOC_S_EDID ioctl, or more easily using `v4l2-ctl --fix-edid-checksums --set-edid=file=filename.txt` (adding the --fix-edid-checksums option means that you don't have to get the checksum values correct in the source file). Generating the required EDID file (a textual hexdump of a binary EDID file) is not too onerous, and there are tools available to generate them, but it is beyond the scope of this page.

As described above, use the `DV_TIMINGS` ioctls to configure the driver to match the incoming video. The easiest approach for this is to use the command `v4l2-ctl --set-dv-bt-timings query`. The driver does support generating the SOURCE_CHANGED events should you wish to write an application to handle a changing source. Changing the output pixel format is achieved by setting it via VIDIOC_S_FMT, however only the pixel format field will be updated as the resolution is configured by the dv timings.

There are a couple of commercially available boards that connect this chip to the Raspberry Pi. The Auvidea B101 and B102 are the most widely obtainable, but other equivalent boards are available.

This driver is loaded using the `config.txt` dtoverlay `tc358743`.

The chip also supports capturing stereo HDMI audio via I2S. The Auvidea boards break the relevant signals out onto a header, which can be connected to the Pi's 40 pin header. The required wiring is:

| Signal   | B101 header | Pi 40 pin header | BCM GPIO  |
|----------|:-----------:|:----------------:|:---------:|
| LRCK/WFS |     7       |       35         |    19     |
| BCK/SCK  |     6       |       12         |    18     |
| DATA/SD  |     5       |       38         |    20     |
| GND      |     8       |       39         |    N/A    |

The `tc358743-audio` overlay is required *in addition to* the `tc358743` overlay. This should create an ALSA recording device for the HDMI audio.
Please note that there is no resampling of the audio. The presence of audio is reflected in the V4L2 control TC358743_CID_AUDIO_PRESENT / "audio-present", and the sample rate of the incoming audio is reflected in the V4L2 control TC358743_CID_AUDIO_SAMPLING_RATE / "Audio sampling-frequency". Recording when no audio is present will generate warnings, as will recording at a sample rate different from that reported.
