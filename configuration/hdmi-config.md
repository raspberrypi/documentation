## HDMI Configuration

In the vast majority of cases, simply plugging your HDMI equipped monitor in to the Raspberry Pi using a standard HDMI cable will just work at the best resolution the monitor supports.

However, there are some circumstances where the Raspberry Pi may not be able to determine the best mode, or you specifically wish to set a non-default resolution.

Note that all the commands on this page are documented fully in the config.txt [Video](config-txt/video.md) documentation.

### HDMI Groups and Mode 

HDMI has two common groups, CEA (Consumer Electronics Association, the standard typically used by TVs) and DMT (Display Monitor Timings, the standard typically used by monitors). Each groups advertises a particular set of modes, where a mode describes the resolution, framerate, clock rate and aspect ratio of the output.

### What modes does my device support?

You can use the `tvservice` command to determine which modes are supported by your device, along with other useful data.

`tvservice -s` Displays the current HDMI status including mode and resolution.  
`tvservice -m CVT` Lists all supported CVT modes  
`tvservice -m DMT` Lists all supported DMT modes  

### Setting a specific HDMI mode

Setting a specific mode is done using the `hdmi_group` and `hdmi_mode` config.txt entries. The group entry selects between CEA or DMT  and the mode selects the resolution and framerate. There are tables of modes on the config.txt [Video](config-txt/video.md) page, but use the `tvservice` command described above to find out exactly which modes your device supports.

### Setting a custom HDMI mode.

There are two optiosn for setting a custom mode,  `hdmi_cvt` and `hdmi_timings`. 

In certain rare cases it may be necessary to define the exact clock requirements of the HDMI signal. This is called a custom mode, and is activated by setting `hdmi_group=2` and `hdmi_mode=87`. You can then use the `hdmi_timings` config.txt command to set the specific parameters for your display. 
`hdmi_timings` specifies all the timings that an HDMI signal needs to use. These timings are usually found is datasheets related to the display being used.

`hdmi_timings=<h_active_pixels> <h_sync_polarity> <h_front_porch> <h_sync_pulse> <h_back_porch> <v_active_pixels> <h_sync_polarity> <h_front_porch> <h_sync_pulse> <h_back_porch> <v_active_lines> <v_sync_polarity> v_front_porch> <v_sync_pulse> <v_back_porch> <v_sync_offset_a> <v_sync_offset_b> <pixel_rep> <frame_rate> <interlaced> <pixel_freq> <aspect_ratio>`

- `h_active_pixels` The horizontal resolution
- `h_sync_polarity` 0 or 1 to define the horizontal sync polarity
- `h_front_porch` Number of horizontal front porch pixels 
- `h_sync_pulse` Width of horizontal sync pulse
- `h_back_porch` Number of horizontal back porch pixels 
- `v_active_lines` The vertical resolution
- `v_sync_polarity` 0 or 1 to define the vertical sync polartty
- `v_front_porch` Number of Vertical  front porch pixels
- `v_sync_pulse` Width of vertical sync pulse
- `v_back_porch` Number of vertical back porch pixels
- `v_sync_offset_a`
- `v_sync_offset_b`
- `pixel_rep`
- `frame_rate` Frame rate of mode
- `interlaced` 0 for non-interlaced, 1 for interlaced
- `pixel_freq` The mode pixel frequency
- `aspect_ratio` ?

### HDMI not working properly.

In some rare cases you may need to increase the HDMI drive strength, for example, speckling on the display, or when using very long cables. There is a config.txt item to do this, `config_hdmi_boost`, which is documented on the config.txt [Video](config-txt/video.md) page.

