# Playing video on the Raspberry Pi

On the Pi 3 and earlier models, the simplest way of playing video is to use the OMXPlayer application, which is described in more detail [in this documentation section](../../raspbian/applications/omxplayer.md).

To play a video, navigate to the location of your video file in the terminal using `cd`, then type the following command:

```bash
omxplayer example.mp4
```

This will play the `example.mp4` in full screen. Hit `Ctrl + C` to exit.

On the Pi 4, hardware support for MPEG2 and VC-1 codecs has been removed, so we recommend the use of the VLC application, which supports these formats in software. In addition, VLC has hardware support for H264 and the new HEVC codec.

## Example video sample: Big Buck Bunny

A video sample of the animated film *Big Buck Bunny* is available on the Pi. To play it on a Pi 3 or earlier models, enter the following command into a terminal window:

```bash
omxplayer /opt/vc/src/hello_pi/hello_video/test.h264
```

On a Pi 4, use the following command for H264 files:

```bash
omxplayer /opt/vc/src/hello_pi/hello_video/test.h264
```
or for H264, VC1, or MPEG2
```bash
vlc /opt/vc/src/hello_pi/hello_video/test.h264
```

When using VLC, you can improve playback performance by encapsulating the raw H264 stream, for example from the Raspberry Pi Camera Module. This is easily done using `ffmpeg`. Playback is also improved if VLC is run full screen; either select fullscreen from the user interface, or you can add the `--fullscreen` options to the `vlc` command line.

This example command converts `video.h264` to a containerised `video.mp4` at 30 fps:

`ffmpeg -r 30 -i video.h264 -c:v copy video.mp4`
