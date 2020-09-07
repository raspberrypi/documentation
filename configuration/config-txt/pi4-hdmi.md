# Raspberry Pi 4 HDMI pipeline

The Raspberry Pi 4 has updated the HDMI composition pipeline in a number of ways
to support up to 4k60 displays. One of the main ones is that it generates 2
output pixels for every clock cycle.

Every HDMI mode has a list of timings that control all the parameters around
sync pulse durations. These are typically defined via a pixel clock, and then a
number of active pixels, a front porch, sync pulse, and back porch for each of the
horizontal and vertical directions.
Running everything at 2 pixels per clock means that the Pi4 can not support a
timing where any of the horizontal timings are not divisible by 2. The firmware
and Linux kernel will now filter out any mode that does not fulfill this
criteria.

There is only one mode in the CEA and DMT standard that falls into this
category - DMT mode 81 1366x768 @ 60Hz.
(1366x768 is already a strange mode as normally the width is divisible by 8, and
1366 isn't).

If your monitor is of this resolution, then the Pi4 will drop down to the next
mode that is advertised by the monitor. Thiis is typically 1280x720.

On some monitors it is possible to configure them to use 1360x768 @ 60Hz. They
typically do not advertise this mode so the selection can't be made
automatically, but it can be manually chosen by adding
```
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1360 768 60
```
to config.txt.

Timings specified manually via a ```hdmi_timings=``` line will also need to
comply with this restriction.

```dpi_timings=``` aren't restricted in the same way as that pipeline still only
runs at a single pixel per clock cycle.