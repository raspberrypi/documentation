# Python picamera

`python-picamera` is a pure Python interface to the Raspberry Pi camera module for Python 2.7 (or above) or Python 3.2 (or above). The library is written and maintained by [Dave Jones](https://github.com/waveform80).

Also see the [camera setup](README.md) page.

## Installation

The `python-picamera` library is available in the Raspbian archives. Install with `apt`:

```
sudo apt-get update
sudo apt-get install python-picamera
```

Alternatively, the Python3 package is installed with `apt-get install python3-picamera`. Also the documentation is available with `apt-get install python-picamera-docs`.

## Usage

First, in the Python prompt or at the top of a Python file, enter:

```
import picamera
```

This will make the library available to the script.

Now create an instance of the PiCamera class:

```
camera = picamera.PiCamera()
```

And take a picture:

```
camera.capture('image.jpg')
```

### Horizontal and Vertical flip

Like with the `raspistill` command, you can apply a horizontal and vertical flip if your camera is positioned upside-down. This is done by changing the `hflip` and `vflip` properties directly:

```
camera.hflip = True
camera.vflip = True
```

Be sure to use an upper case `T` in `True` as this is a keyword in Python.

### Preview

You can open a preview window showing the camera feed on screen (note this will overlay your Python window if you're using the Pi desktop):

```
camera.start_preview()
```

Then use the `stop_preview` method to end:

```
camera.stop_preview()
```

If the preview overlays your Python window you can still type this (blindly) and it should break out of the preview.

Alternatively, you can access the Pi using [SSH](../../remote-access/ssh/README.md) from another computer, open a Python prompt and enter these commands, displaying the preview on a monitor connected to the Pi (not the computer you're connected from).

### Camera settings

You can change other camera configuration by editing property values, for example:

```
camera.brightness = 70
```

This will change the brightness setting from its default `50` to `70` (values between 0 and 100).

Other settings are available. Here is a list with their default values:

```
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
```

### Sleep

You can add pauses between commands using `sleep` from the `time` module:

```
import picamera
from time import sleep

camera = picamera.PiCamera()

camera.capture('image1.jpg')
sleep(5)
camera.capture('image2.jpg')
```

You can also use `sleep` in a preview to adjust settings over time:

```
camera.start_preview()

for i in range(100):
    camera.brightness = i
    sleep(0.2)
```

### Video recording

Record 5 seconds of video:

```
camera.start_recording('video.h264')
sleep(5)
camera.stop_recording()
```

## Documentation

Full documentation for `python-picamera` is available at [picamera.readthedocs.org](http://picamera.readthedocs.org/)

## Development

The `python-picamera` project is written and maintained by [Dave Jones](https://github.com/waveform80) and the source can be found at [github.com/waveform80/picamera](https://github.com/waveform80/picamera) where you can open issues or create pull requests.
