# OMXPlayer Usage

OMXPLayer is a command line hardware accelerated media player that uses the Raspberry Pi's inbuild hardware (part of the Videocore4 GPU), to provide decoding for a variety of formats, both audio and video. 

You can display all the options available using `omxplayer -h`, th next sections describe some of the more interesting options in more detail!

## Playing back video

In its simplest form, you can simply type ```omxplayer <name of file>```. On a default Raspbian install, there is an example H264 video file, so to play this we can do the following in a terminal.

```omxplayer /opt/vc/src/hello_pi/hello_video/test.h264```

You will see that some information is output to the terminal, this shows the codec being used to decode the video, in this case omx-h264 as the file is H264 encoded, along with the size of the video. By default, OMXPlayer plays back at 25fps if no information is available in the file to sepcify otherwise. H264 files do not contain any frame rate information, so the default is used.

By default video playback will expand the playback to fill the display, but retaining the aspect ratio. You can override this beahviour and playback the video in a specific window using the `--win` command line paramter.

```omxplayer -win 50,50,300,300 /opt/vc/src/hello_pi/hello_video/test.h264```

This will normally break the aspect ratio, but you can maintain it with the `--aspect_mode` parameter.

```omxplayer --win 50,50,300,300 --aspect-mode letterbox /opt/vc/src/hello_pi/hello_video/test.h264```

You can also specify which part of the video you wish to display using the `--crop` parameter, this gives a zoom effect.

```omxplayer --crop 50,50,300,300 /opt/vc/src/hello_pi/hello_video/test.h264```

Rotation of the video is possible, but only for 90,180, or 270 degrees, using the `--orientation` parameter.

```omxplayer --orientation 180 /opt/vc/src/hello_pi/hello_video/test.h264```

It's also possible to change the opacity of the video, so you can see whatever is underneath it. Use the `--alpha` parameter to change the opacity, this takes a value from 0 (transparent) to 255 (fully opaque)

```omxplayer --alpha 128 /opt/vc/src/hello_pi/hello_video/test.h264```

## Keyboard Control

You can control OMXPlayer when running using various keyboard command. note that not all commands will work will all media.

| Key | Command |
|---|----------------|
| 1 | decrease speed |
| 2 | increase speed |
| < | rewind |
| > | fast forward |
| z | show info |
| j | previous audio stream |
| k | next audio stream |
| i | previous chapter | 
| o | next chapter |
| n | previous subtitle stream |
| m | next subtitle stream |
| s | toggle subtitles |
| w | show subtitles |
| x | hide subtitles |
| d | decrease subtitle delay (- 250 ms) |
| f | increase subtitle delay (+ 250 ms) |
| q |  exit omxplayer |
| p / space | pause/resume |
| - | decrease volume |
|  + / = | increase volume |
| left arrow | seek -30 seconds |
| right arrow | seek +30 seconds |
| down arrow | seek -600 seconds |
| up arrow | seek +600 seconds |

## It's not working!

If OMXPlayer does not recognise the format of the stream it is being asked to play, it will exit immediately with the message "Have a nice day;)". 

If you are playing back over the HDMI and there is no audio, try the -o,--adev option, which is used to specify the audio output device

```omxplayer -o hdmi <media file>```











