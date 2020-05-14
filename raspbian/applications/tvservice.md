## tvservice

`tvservice` is a command line application used to get and set information about the display, targeted mainly at HDMI video and audio.

Typing `tvservice` by itself will display a list of available command line options.

### Options

#### -p, --preferred

Power on the HDMI output with preferred settings.

#### -o, --off

Powers off the display output. 

**Important Note:** Powering off the output using this command will also destroy any framebuffers/dispmanx layers associated with the display. These are NOT re-established with a subsequent power on, so will result in a blank screen. 

A better option is to use the [vcgencmd display_power](vcgencmd.md) option, as this will retain any framebuffers, so when the power is turned back on the display will be the returned to the previous power on state.

#### -e, --explicit="Group Mode Drive"

Power on the HDMI with the specified settings

Group can be one of `CEA`, `DMT`, `CEA_3D_SBS`, `CEA_3D_TB`, `CEA_3D_FP`, `CEA_3D_FS`.  
Mode is one of the modes returned from the `-m, --modes` option.  
Drive can be one of `HDMI`, `DVI`.  

#### -t, --ntsc

Use 59.94Hz (NTSC frequency) rather than 60Hz for HDMI mode.

#### -c, --sdtvon="Mode Aspect [P]"

Power on the SDTV (composite output) with the specified mode, `PAL` or `NSTC`, and the specified aspect, `4:3`, `14:9`, `16:9`. The optional `P` parameter can be used to specify progressive mode. 

#### -m, --modes=Group

where Group is `CEA` or `DMT`.

Shows a list of display modes available in the specified group.

#### -M, --monitor

Monitors for any HDMI events, for example unplugging or attaching.

#### -s, --status

Shows the current settings for the display mode, including mode, resolution, and frequency.

#### -a, --audio

Shows the current settings for the audio mode, including channels, sample rate and sample size.

#### -d, --dumpid=filename

Save the current EDID to the specified filename. You can then use `edidparser <filename>` to display the data in a human readable form. 

#### -j, --json

When used in combination with the `--modes` options, displays the mode information in JSON format. 

#### -n, --name

Extracts the display name from the EDID data and shows it.


