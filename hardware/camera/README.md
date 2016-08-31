# Camera Module

The Raspberry Pi camera module is an official product from the Raspberry Pi Foundation. The original 5-megapixel model was [released](https://www.raspberrypi.org/blog/camera-board-available-for-sale/) in 2013, and an 8-megapixel V2 was [released](https://www.raspberrypi.org/blog/new-8-megapixel-camera-board-sale-25/) in 2016. For both iterations of the camera there are visible light and infra-red versions.

## Hardware specification

| | Camera V1 | Camera V2 |
| --- | --- | --- |
| Net price | $25 | $25 |
| Size | around 25 x 24 x 9 mm | |
| Weight | 3g | |
| Still resolution | 5 Megapixels | 8 Megapixels |
| Video modes | 1080p30, 720p60 and 640x480p60/90 | 1080p30, 720p60 and 640x480p60/90 |
| Linux integration | V4L2 driver available | V4L2 driver available |
| C programming API | OpenMAX IL and others available | OpenMAX IL and others available |
| Sensor | OmniVision OV5647 | [Sony IMX219](http://www.sony.net/Products/SC-HP/new_pro/april_2014/imx219_e.html) |
| Sensor resolution | 2592 x 1944 pixels | 3280 x 2464 pixels |
| Sensor image area | 3.76 x 2.74 mm | |
| Pixel size | 1.4 µm x 1.4 µm | |
| Optical size	| 1/4" | |
| Full-frame SLR lens equivalent | 35 mm | |
| S/N ratio | 36 dB | |
| Dynamic range | 67 dB @ 8x gain | |
| Sensitivity | 680 mV/lux-sec | |
| Dark current | 16 mV/sec @ 60 C | |
| Well capacity | 4.3 Ke- | |
| Fixed focus | 1 m to infinity | |
| Focal length | 3.60 mm +/- 0.01 | |
| Horizontal field of view | 53.50  +/- 0.13 degrees | |
| Vertical field of view | 41.41 +/- 0.11 degrees | |
| Focal ratio (F-Stop) | 2.9 | |

## Hardware features

| Available | Implemented |
| --- | --- |
| Chief ray angle correction | Yes |
| Global and rolling shutter | Rolling shutter |
| Automatic exposure control (AEC) | No - done by ISP instead |
| Automatic white balance (AWB) | No - done by ISP instead |
| Automatic black level calibration (ABLC) | No - done by ISP instead |
| Automatic 50/60 Hz luminance detection | No - done by ISP instead |
| Frame rate up to 120 fps | max 90fps. Limitations on frame size for the higher frame rates (VGA only for above 47fps) |
| AEC/AGC 16-zone size/position/weight control | No - done by ISP instead |
| Mirror and flip | Yes |
| Cropping | No - done by ISP instead (except 1080p mode) |
| Lens correction | No - done by ISP instead |
| Defective pixel cancelling | No - done by ISP instead |
| 10-bit RAW RGB data | Yes - format conversions available via GPU |
| Support for LED and flash strobe mode | LED flash |
| Support for internal and external frame synchronisation for frame exposure mode | No |
| Support for 2x2 binning for better SNR in low light conditions | Anything output res below 1296x976 will use the 2x2 binned mode |
| Support for horizontal and vertical sub-sampling | Yes, via binning and skipping |
| On-chip phase lock loop (PLL) | Yes |
| Standard serial SCCB interface | Yes |
| Digital video port (DVP) parallel output interface | No |
| MIPI interface (two lanes) | Yes |
| 32 bytes of embedded one-time programmable (OTP) memory | No |
| Embedded 1.5V regulator for core power | Yes |

## Software features

Full camera software documentation can be found at [raspbian/applications/camera](../../raspbian/applications/camera.md).

| | |
| --- | --- |
| Picture formats | JPEG (accelerated), JPEG + RAW, GIF, BMP, PNG, YUV420, RGB888 |
| Video formats | raw h.264 (accelerated) |
| Effects | negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation |
| Exposure modes |auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks |
| Metering modes | average, spot, backlit, matrix |
| Automatic white balance modes | off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon |
| Triggers | Keypress, UNIX signal, timeout |
| Extra modes | demo, burst/timelapse, circular buffer, video with motion vectors, segmented video, live preview on 3D models |

## Mechanical drawing

- Camera module V2 [PDF](rpi-cam-v2_1-dimensions.pdf)
