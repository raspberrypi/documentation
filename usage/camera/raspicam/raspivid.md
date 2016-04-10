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

### MP4 Video Format

The Pi captures video as a raw H264 video stream. Many media players will refuse to play it (or play it at an incorrect speed) unless it is "wrapped" in a suitable container format like MP4. The easiest way to obtain an MP4 file from the raspivid command is using MP4Box.

First install MP4Box with this command:

```bash
sudo apt-get install -y gpac
```

Then capture your raw video with raspivid and wrap it in an MP4 container all at once this:

```bash
raspivid -t 30000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480 -o pivideo.h264 && MP4Box -add pivideo.h264 pivideo.mp4 && rm pivideo.h264
```

(the above command captures a 30 second video at 640x480 size with a 150kB/s bitrate, then adds an MP4 wrapper and removes the original raw video file afterwards) 

Or simply wrap MP4 around your existing raspivid output like this:

```bash
MP4Box -add video.h264 video.mp4
```

## Full documentation

Full documentation of the camera can be found at [hardware/camera](../../../hardware/camera.md).
