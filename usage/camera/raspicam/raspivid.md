# raspivid

`raspivid` is the command line tool for capturing video with the camera module.

## Basic usage

To record a video with the camera module, use the following command:

```
raspivid -o vid.h264
```

This will save a 5 second video file to the path given here as `vid.h264` (default length of time).

### Specify length of video

To specify the length of the video taken, pass in the `-t` flag with a number of milliseconds. For example:

```
raspivid -o video.h264 -t 10000
```

This will record 10 seconds of video.

### More options

For a full list of possible options, run `raspivid` with no arguments, or pipe this command through `less` and scroll through:

```
raspivid | less
```

Use the arrow keys to scroll and type `q` to exit.

## Streaming video

View the guide on streaming the video feed on your computer depending on your Operating System:

- [Linux](streaming/linux.md)
- [Mac OS](streaming/mac.md)
- [Windows](streaming/windows.md)

## Full documentation

Full documentation of the camera can be found at [hardware/camera](../../../hardware/camera.md).
