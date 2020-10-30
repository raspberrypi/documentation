## The V4L2 driver

The V4L2 driver provides a standard Linux driver for accessing camera features: this is the driver needed to use a Raspberry Pi camera as, for example, a webcam. The V4L2 driver provides a standard API on top of the firmware-based camera system.

### Installing the V4L2 driver

Installation of the V4L2 driver is automatic. It is loaded as a child of the VCHIQ driver, and once loaded it will check how many cameras are attached and then create the right number of device nodes.

| \dev\videoX | Default Action |
|-------------|:--------------:|
| video10     | Decode |
| video11     | Encode |
| video12     | Simple ISP |
| video13     | Full ISP In |
| video14     | Full ISP Hi-res Out |
| video15     | Full ISP Lo-res Out | |
| video16     | Full ISP statistics |
| video19     | HEVC Decode |

### Testing the driver

There are many Linux applications that use the V4L2 API. The kernel maintainers provide a test tool called `Qv4l2` which can be installed from the Raspberry Pi OS repositories as follows:

`sudo apt install Qv4l2`

### Using the driver

Please see the [V4L2 documentation](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/v4l2.html) for details on using this driver.

