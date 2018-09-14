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

Setting a specific mode is done using the `hdmi_group` and `hdmi_mode` config.txt entries. The group entry selects between CEA or DMT  and the mode selects the resolution and framerate. There are tables of modes on the config.txt [Video](config-txt/video.md) page, but use the `tvservice` command described above to find out exactly which mode your device supports.

### Setting a custom HDMI mode.

There are two optiosn for setting a custom mode,  `hdmi_cvt` and `hdmi_timings`. 

In certain rare cases it may be necessary to define the exact clock requirements of the HDMI signal. This is called a custom mode, and is activated by setting `hdmi_group=2` and `hdmi_mode=87`. You can then use the `hdmi_timings` config.txt command to set the specific parameters for your display. 



### HDMI not working properly.

In some rare cases you may need to increase the HDMI drive strength, for example, speckling on the display, or when using very long cables. There is a config.txt item to do this, `config_hdmi_boost`, wihch is documented on the config.txt [Video](config-txt/video.md) page.

