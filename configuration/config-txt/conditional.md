## Conditional filters in config.txt

When a single SD card (or card image) is being used with one Pi and one monitor, it is easy to set `config.txt` as required for that specific combination and keep it that way, amending it only when something changes.


However, if one Pi is swapped between different monitors, or if the SD card (or card image) is being swapped between multiple Pis, a single set of settings may no longer be sufficient. Conditional filters allow you to define certain sections of the config file to be used only in specific cases, allowing a single `config.txt` to create different configurations when read by different hardware.

### The `[all]` filter

This is the most basic filter. It resets all previously set filters and allows any settings listed below it to be applied to all hardware.


    [all]

It is usually a good idea to add an `[all]` filter at the end of groups of filtered settings to avoid unintentionally combining filters (see below).

### The `[pi1]` and `[pi2]` (etc.) filters

Any settings below a `[pi1]` filter will only be applied to Pi 1 (A, A+, B, B+) hardware, including the original Compute Module.
Any settings below a `[pi2]` filter will only be applied to Pi 2 hardware. The `[pi3]` filter is applicable to Pi 3 and Compute Module 3 hardware, while `[pi0]` covers Pi Zero and Pi Zero W.

    [pi1]
    [pi2]
    [pi3]
    [pi0]

These are particularly useful for defining different `kernel`, `initramfs`, and `cmdline` settings, as the Pi 1 and Pi 2 require different kernels. They can also be useful to define different overclocking settings, as the Pi 1 and Pi 2 have different default speeds. For example, to define separate `initramfs` images for each:

    [pi1]
    initramfs initrd.img-3.18.7+ followkernel
    [pi2]
    initramfs initrd.img-3.18.7-v7+ followkernel
    [all]

Remember to use the `[all]` filter at the end, so that any subsequent settings aren't limited to Pi 2 hardware only.

### The `[none]` filter

The `[none]` filter prevents any settings that follow from being applied to any hardware. Although there is nothing that you can't do without `[none]`, it can be a useful way to keep groups of unused settings in config.txt without having to comment out every line.

    [none]

### The `[EDID=*]` filter

When switching between multiple monitors while using a single SD card in your Pi, and where a blank config isn't sufficient to automatically select the desired resolution for each one, this allows specific settings to be chosen based on the monitors' EDID names.

To view the EDID name of a specific monitor, run the following command:

    tvservice -n

This will print something like this:

    device_name=VSC-TD2220

You can then specify settings that apply only to this monitor:

    [EDID=VSC-TD2220]
    hdmi_group=2
    hdmi_mode=82
    [all]

This forces 1920x1080 DVT mode for the specified monitor, without affecting any other monitors.

Note that these settings apply only at boot, so the monitor must be connected at boot time and the Pi must be able to read its EDID information to find the correct name. Hotplugging a different monitor into the Pi after boot will not select different settings.

### The serial number filter

Sometimes settings should only be applied to a single specific Pi, even if you swap the SD card to a different one. Examples include licence keys and overclocking settings (although the licence keys already support SD card swapping in a different way). You can also use this to select different display settings, even if the EDID identification above is not possible, provided that you don't swap monitors between your Pis. For example, if your monitor doesn't supply a usable EDID name, or if you are using composite output (for which EDID cannot be read).

To view the serial number of your Pi, run the following command:

    cat /proc/cpuinfo

The serial will be shown as a 16-digit hex value at the bottom. For example, if you see:

    Serial          : 0000000012345678

then you can define settings that will only be applied to this specific Pi:

    [0x12345678]
    # settings here are applied only to the Pi with this serial
    [all]
    # settings here are applied to all hardware

### Combining conditional filters

Filters of the same type replace each other, so `[pi2]` overrides `[pi1]`, because it is not possible for both to be true at once.

Filters of different types can be combined simply by listing them one after the other, for example:

    # settings here are applied to all hardware
    [EDID=VSC-TD2220]
    # settings here are applied only if monitor VSC-TD2220 is connected
    [pi2]
    # settings here are applied only if monitor VSC-TD2220 is connected *and* on a Pi 2
    [all]
    # settings here are applied to all hardware

Use the `[all]` filter to reset all previous filters and avoid unintentionally combining different filter types.





*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
