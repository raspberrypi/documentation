## HDMI configuration

For the Pi3 and earlier, in the vast majority of cases, simply plugging your HDMI-equipped monitor into the Raspberry Pi using a standard HDMI cable will automatically lead to the Pi using best resolution the monitor supports.

For the Pi4, which has two micro HDMI ports, you have to ability to attach two 1080p displays, or one 4k display (to either HDMI port). You will need a micro to full size HDMI lead, or a micro to HDMI adapter. If your display supports 4K resolutions you will need to enable 4K output by setting the `hdmi_enable_4k=1` flag in config.txt or using the Raspberry Pi Configuration tool. The Pi4 should automatically detect the best resolution to display.

However, there are some circumstances in which the Raspberry Pi may not be able to determine the best mode, or you specifically wish may to set a non-default resolution. This rest of this page describes what you need to do to achieve this.

Note that all the commands on this page are documented fully in the config.txt [Video](config-txt/video.md) documentation.

### HDMI groups and mode 

HDMI has two common groups: CEA (Consumer Electronics Association, the standard typically used by TVs) and DMT (Display Monitor Timings, the standard typically used by monitors). Each group advertises a particular set of modes, where a mode describes the resolution, frame rate, clock rate, and aspect ratio of the output.

### What modes does my device support?

You can use the `tvservice` application on the command line to determine which modes are supported by your device, along with other useful data:

+ `tvservice -s` displays the current HDMI status, including mode and resolution
+ `tvservice -m CVT` lists all supported CVT modes  
+ `tvservice -m DMT` lists all supported DMT modes  

If you are using a Pi4 with more than one display attached, then `tvservice` needs to be told which device to ask for information. You can get display ID's for all attached devices by using: 

`tvservice -l`

You can specify which display `tvservice` uses by adding `-v <display id>` to the `tvservice` command. e.g.

+ `tvservice -v 7 -m CVT` lists all supported CVT modes for display ID 7.

### Setting a specific HDMI mode

Setting a specific mode is done using the `hdmi_group` and `hdmi_mode` config.txt entries. The group entry selects between CEA or DMT, and the mode selects the resolution and frame rate. You can find tables of modes on the config.txt [Video Configuration](config-txt/video.md) page, but you should use the `tvservice` command described above to find out exactly which modes your device supports.

Fot the Pi4, to specifiy the HDMI port, you can add an index indentifier to the `hdmi_group` or `hdmi_mode` entry in config.txt. e.g. `hdmi_mode:0` or `hdmi_group:1`.


### Setting a custom HDMI mode.

There are two options for setting a custom mode: `hdmi_cvt` and `hdmi_timings`. 

`hdmi_cvt` sets a custom Coordinated Video Timing entry, which is described fully here: [Video Configuration](config-txt/video.md#Custom%20Mode)

In certain rare cases it may be necessary to define the exact clock requirements of the HDMI signal. This is a fully custom mode, and it is activated by setting `hdmi_group=2` and `hdmi_mode=87`. You can then use the `hdmi_timings` config.txt command to set the specific parameters for your display. 
`hdmi_timings` specifies all the timings that an HDMI signal needs to use. These timings are usually found in the datasheet of the display being used.

`hdmi_timings=<h_active_pixels> <h_sync_polarity> <h_front_porch> <h_sync_pulse> <h_back_porch> <v_active_pixels> <h_sync_polarity> <h_front_porch> <h_sync_pulse> <h_back_porch> <v_active_lines> <v_sync_polarity> v_front_porch> <v_sync_pulse> <v_back_porch> <v_sync_offset_a> <v_sync_offset_b> <pixel_rep> <frame_rate> <interlaced> <pixel_freq> <aspect_ratio>`

| Timing        | Purpose       |
| ------------- | ------------- |
| `h_active_pixels`     | The horizontal resolution |
| `h_sync_polarity`     | 0 or 1 to define the horizontal sync polarity      | 
| `h_front_porch` | Number of horizontal front porch pixels      |
| `h_sync_pulse` | Width of horizontal sync pulse    |
| `h_back_porch` | Number of horizontal back porch pixels    | 
| `v_active_lines` | The vertical resolution    | 
| `v_sync_polarity` | 0 or 1 to define the vertical sync polarity      | 
| `v_front_porch` | Number of vertical front porch pixels     | 
| `v_sync_pulse` | Width of vertical sync pulse     | 
| `v_back_porch` | Number of vertical back porch pixels     | 
| `v_sync_offset_a` | Leave at 0     | 
| `v_sync_offset_b` | Leave at 0     | 
| `pixel_rep` | Leave at 0     | 
| `frame_rate` | Frame rate of mode      |
| `interlaced` | 0 for non-interlaced, 1 for interlaced    | 
| `pixel_freq` | The mode pixel frequency     | 
| `aspect_ratio` | The aspect ratio required      | 

`aspect_ratio` should be one of the following:

| Ratio | `aspect_ratio` ID |
|-------|----|
| `4:3` | 1  |  
|`14:9` | 2  |
|`16:9` | 3  |
|`5:4`  | 4  |
|`16:10`| 5  | 
|`15:9` | 6  |
|`21:9` | 7  |
|`64:27`| 8  |

Fot the Pi4, to specifiy the HDMI port, you can add an index indentifier to the config.txt. e.g. `hdmi_cvt:0=...` or `hdmi_timings:1=...`.

### HDMI not working properly?

In some rare cases you may need to increase the HDMI drive strength, for exampl when there is speckling on the display, or when you are using very long cables. There is a config.txt item to do this, `config_hdmi_boost`, which is documented on the config.txt [Video](config-txt/video.md) page.

The Pi4 does not support 'config_hdmi_boost'.

