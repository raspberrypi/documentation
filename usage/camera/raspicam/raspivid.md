# raspivid

`raspivid` is the command line tool for capturing video with a Raspberry Pi camera module.

## Basic usage of raspivid

With a camera module [connected and enabled](../README.md), record a video using the following command:

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

### MP4 Video Format

The Pi captures video as a raw H264 video stream. Many media players will refuse to play it, or play it at an incorrect speed, unless it is "wrapped" in a suitable container format like MP4. The easiest way to obtain an MP4 file from the raspivid command is using MP4Box.

Install MP4Box with this command:

```bash
sudo apt install -y gpac
```

Capture your raw video with raspivid and wrap it in an MP4 container like this:

```bash
# Capture 30 seconds of raw video at 640x480 and 150kB/s bit rate into a pivideo.h264 file:
raspivid -t 30000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480 -o pivideo.h264 
# Wrap the raw video with an MP4 container: 
MP4Box -add pivideo.h264 pivideo.mp4
# Remove the source raw file, leaving the remaining pivideo.mp4 file to play
rm pivideo.h264
```

Alternatively, wrap MP4 around your existing raspivid output, like this:

```bash
MP4Box -add video.h264 video.mp4
```

## Full documentation

Full documentation of the camera can be found at [hardware/camera](../../../hardware/camera/README.md).
