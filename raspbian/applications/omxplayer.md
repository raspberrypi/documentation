# OMXPlayer: An accelerated command line media player

Installed on Raspberry Pi OS is a command line media player, called OMXPlayer. This is HW accelerated, and can play back many popular audio and video file formats.

OMXPlayer was developed by the Kodi project's Edgar Hucek.

OMXPlayer uses the OpenMAX (omx) hardware acceleration interface (API) which is the officially supported media API on the Raspberry Pi.

## Basic usage

The simplest command line is `omxplayer <name of media file>`. The media file can be audio or video or both. For the examples below, we used an H264 video file that is included with the standard Raspberry Pi OS installation.

```
omxplayer /opt/vc/src/hello_pi/hello_video/test.h264
```

By default the audio is sent to the analog port. If you are using a HDMI-equipped display device with speakers, you need to tell omxplayer to send the audio signal over the HDMI link.

```
omxplayer --adev hdmi /opt/vc/src/hello_pi/hello_video/test.h264
```

When displaying video, the whole display will be used as output. You can specify which part of the display you want the video to be on using the window option.

```
omxplayer --win 0,0,640,480 /opt/vc/src/hello_pi/hello_video/test.h264
```

You can also specify which part of the video you want to be displayed: this is called a crop window. This portion of the video will be scaled up to match the display, unless you also use the window option.

```
omxplayer --crop 100,100,300,300 /opt/vc/src/hello_pi/hello_video/test.h264
```
If you are using the Raspberry Pi Foundation's touchscreen display, and you want to use it for video output, use the display option to specify which display to use. `n` is 5 for HDMI, 4 for the touchscreen. With the Raspberry Pi 4 you have two options for HDMI output. `n` is 2 for HDMI0 and 7 for HDMI1.

```
omxplayer --display n /opt/vc/src/hello_pi/hello_video/test.h264
```
## Options available during playback

There are a number of options available during playback, actioned by pressing the appropriate key. Not all options will be available on all files. The list of key bindings can be displayed using `omxplayer --keys`:

```
    1           decrease speed
    2           increase speed
    <           rewind
    >           fast forward
    z           show info
    j           previous audio stream
    k           next audio stream
    i           previous chapter
    o           next chapter
    n           previous subtitle stream
    m           next subtitle stream
    s           toggle subtitles
    w           show subtitles
    x           hide subtitles
    d           decrease subtitle delay (- 250 ms)
    f           increase subtitle delay (+ 250 ms)
    q           exit omxplayer
    p / space   pause/resume
    -           decrease volume
    + / =       increase volume
    left arrow  seek -30 seconds
    right arrow seek +30 seconds
    down arrow  seek -600 seconds
    up arrow    seek +600 seconds

```

## All command line options

This is a full list of options available in the build from 23rd September 2016, displayed using `omxplayer --help`:

```
 -h  --help                  Print this help
 -v  --version               Print version info
 -k  --keys                  Print key bindings
 -n  --aidx  index           Audio stream index    : e.g. 1
 -o  --adev  device          Audio out device      : e.g. hdmi/local/both/alsa[:device]
 -i  --info                  Dump stream format and exit
 -I  --with-info             dump stream format before playback
 -s  --stats                 Pts and buffer stats
 -p  --passthrough           Audio passthrough
 -d  --deinterlace           Force deinterlacing
     --nodeinterlace         Force no deinterlacing
     --nativedeinterlace     let display handle interlace
     --anaglyph type         convert 3d to anaglyph
     --advanced[=0]          Enable/disable advanced deinterlace for HD videos (default enabled)
 -w  --hw                    Hw audio decoding
 -3  --3d mode               Switch tv into 3d mode (e.g. SBS/TB)
 -M  --allow-mvc             Allow decoding of both views of MVC stereo stream
 -y  --hdmiclocksync         Display refresh rate to match video (default)
 -z  --nohdmiclocksync       Do not adjust display refresh rate to match video
 -t  --sid index             Show subtitle with index
 -r  --refresh               Adjust framerate/resolution to video
 -g  --genlog                Generate log file
 -l  --pos n                 Start position (hh:mm:ss)
 -b  --blank[=0xAARRGGBB]    Set the video background color to black (or optional ARGB value)
     --loop                  Loop file. Ignored if file not seekable
     --no-boost-on-downmix   Don't boost volume when downmixing
     --vol n                 set initial volume in millibels (default 0)
     --amp n                 set initial amplification in millibels (default 0)
     --no-osd                Do not display status information on screen
     --no-keys               Disable keyboard input (prevents hangs for certain TTYs)
     --subtitles path        External subtitles in UTF-8 srt format
     --font path             Default: /usr/share/fonts/truetype/freefont/FreeSans.ttf
     --italic-font path      Default: /usr/share/fonts/truetype/freefont/FreeSansOblique.ttf
     --font-size size        Font size in 1/1000 screen height (default: 55)
     --align left/center     Subtitle alignment (default: left)
     --no-ghost-box          No semitransparent boxes behind subtitles
     --lines n               Number of lines in the subtitle buffer (default: 3)
     --win 'x1 y1 x2 y2'     Set position of video window
 --win x1,y1,x2,y2       Set position of video window
 --crop 'x1 y1 x2 y2'    Set crop area for input video
 --crop x1,y1,x2,y2      Set crop area for input video
 --aspect-mode type      Letterbox, fill, stretch. Default is stretch if win is specified, letterbox otherwise
 --audio_fifo  n         Size of audio output fifo in seconds
 --video_fifo  n         Size of video output fifo in MB
 --audio_queue n         Size of audio input queue in MB
 --video_queue n         Size of video input queue in MB
 --threshold   n         Amount of buffered data required to finish buffering [s]
 --timeout     n         Timeout for stalled file/network operations (default 10s)
 --orientation n         Set orientation of video (0, 90, 180 or 270)
 --fps n                 Set fps of video where timestamps are not present
 --live                  Set for live tv or vod type stream
 --layout                Set output speaker layout (e.g. 5.1)
 --dbus_name name        default: org.mpris.MediaPlayer2.omxplayer
 --key-config <file>     Uses key bindings in <file> instead of the default
 --alpha                 Set video transparency (0..255)
 --layer n               Set video render layer number (higher numbers are on top)
 --display n             Set display to output to
 --cookie 'cookie'       Send specified cookie as part of HTTP requests
 --user-agent 'ua'       Send specified User-Agent as part of HTTP requests
 --lavfdopts 'opts'      Options passed to libavformat, e.g. 'probesize:250000,...'
 --avdict 'opts'         Options passed to demuxer, e.g., 'rtsp_transport:tcp,...'

```
