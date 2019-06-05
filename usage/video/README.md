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

For Pi4, you can use the following for H264 files,

```bash
omxplayer --no-osd /opt/vc/src/hello_pi/hello_video/test.h264
```
or for H264, VC1, or MPEG2
```bash
vlc /opt/vc/src/hello_pi/hello_video/test.h264
```

When using VLC, you can improve playback performance by encapsulating raw H264 stream from, for example, the Raspberry Pi camera. This is easily done with `ffmpeg`.

This example converts `video.h64` to a containerised `video.mp4`, at 30 fps.

`ffmpeg -r 30 -i video.h265 -c:v copy video.mp4`


