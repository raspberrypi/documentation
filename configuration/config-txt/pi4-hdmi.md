# Raspberry Pi 4 HDMI pipeline

In order to support dual displays, and modes up to 4k60, the Raspberry Pi 4 has updated the HDMI composition pipeline hardware in a number of ways. One of the major changes is that it generates 2 output pixels for every clock cycle.

Every HDMI mode has a list of timings that control all the parameters around sync pulse durations. These are typically defined via a pixel clock, and then a number of active pixels, a front porch, sync pulse, and back porch for each of the horizontal and vertical directions. 

Running everything at 2 pixels per clock means that the Pi4 can not support a timing where _any_ of the horizontal timings are not divisible by 2. The firmware and Linux kernel will filter out any mode that does not fulfill this criteria.

There is only one mode in the CEA and DMT standards that falls into this category - DMT mode 81, which is 1366x768 @ 60Hz. This mode has odd values for the horizontal sync and back porch timings. It's also an unusual mode for having a width that isn't divisible by 8.

If your monitor is of this resolution, then the Pi4 will automatically drop down to the next mode that is advertised by the monitor; this is typically 1280x720.

On some monitors it is possible to configure them to use 1360x768 @ 60Hz. They typically do not advertise this mode via their EDID so the selection can't be made automatically, but it can be manually chosen by adding

```
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1360 768 60
```
to [config.txt](./video.md).

Timings specified manually via a `hdmi_timings=` line in `config.txt` will also need to comply with the restriction of all horizontal timing parameters being divisible by 2.

`dpi_timings=` are not restricted in the same way as that pipeline still only runs at a single pixel per clock cycle.
