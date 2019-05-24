# Playing video on the Raspberry Pi

On the Pi3 or earlier, the simplest way of playing video is to use the OMXPlayer application, which is described in more detail [here](../../raspbian/applications/omxplayer.md).

To play a video, navigate to the location of your video file in the terminal using `cd`, then type the following command:

```bash
omxplayer example.mp4
```

This will play the `example.mp4` in full screen. Hit `Ctrl + C` to exit.

On the Pi4, HW support for MPEG2 and VC-1 codecs has been removed, so we recomend the use of VLC, which will support those formats in software. In addition, VLC has hardware support for H264 and the new HEVC codec.

## Example video sample: Big Buck Bunny

There is a video sample of the animated film *Big Buck Bunny* available on the Pi. To play on a Pi3 or earlier, enter the following command into the terminal:

```bash
omxplayer /opt/vc/src/hello_pi/hello_video/test.h264
```

For Pi4, use

```bash
vlc /opt/vc/src/hello_pi/hello_video/test.h264
```

