# raspivid

`raspivid` is the command line tool for capturing video with the camera module.

## Basic usage of raspivid

With the camera module [connected and enabled](../README.md), record a video using the following command:

```bash
raspivid -o vid.h264
```

Remember to use `-hf` and `-vf` to flip the image if required, like with [raspistill](raspistill.md)

This will save a 5 second video file to the path given here as `vid.h264` (default length of time).

### Specify length of video

To specify the length of the video taken, pass in the `-t` flag with a number of milliseconds. For example:

```bash
raspivid -o video.h264 -t 10000
```

This will record 10 seconds of video.

### More options

For a full list of possible options, run `raspivid` with no arguments, or pipe this command through `less` and scroll through:

```bash
raspivid 2>&1 | less
```

Use the arrow keys to scroll and type `q` to exit.

## Full documentation

Full documentation of the camera can be found at [hardware/camera](../../../hardware/camera/README.md).
