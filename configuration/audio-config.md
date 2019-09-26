# Audio configuration

The Raspberry Pi has two audio output modes: HDMI and headphone jack. You can switch between these modes at any time.

If your HDMI monitor or TV has built-in speakers, the audio can be played over the HDMI cable, but you can switch it to a set of headphones or other speakers plugged into the headphone jack. If your display claims to have speakers, sound is output via HDMI by default; if not, it is output via the headphone jack. This may not be the desired output setup, or the auto-detection is inaccurate, in which case you can manually switch the output.

## Changing the audio output

There are three ways of setting the audio output.

### Desktop volume control

Right-clicking the volume icon on the desktop taskbar brings up the audio output selector; this allows you to select between the internal audio outputs. It also allows you to select any external audio devices, such as USB sound cards and Bluetooth audio devices. A green tick is shown against the currently selected audio output device — simply left-click the desired output in the pop-up menu to change this. The volume control and mute operate on the currently selected device.

### Command line

The following command, entered in the command line, will switch the audio output to HDMI:

```
amixer cset numid=3 2
```

Here the output is being set to `2`, which is HDMI. Setting the output to `1` switches to analogue (headphone jack). The default setting is `0` which is automatic.

### raspi-config

Open up [raspi-config](raspi-config.md) by entering the following into the command line:

```
sudo raspi-config
```

This will open the configuration screen:

![raspi-config screen](images/raspi-config.png)

Select `Advanced Options` (here shown as Option 7, but yours may be different) and press `Enter`.

Now select the Option named, `Audio` (here shown as A6, but yours may be different) and press `Enter`:

![Audio configuration screen](images/raspi-config-audio.png)

Now you are presented with the two modes explained above as an alternative to the default `Auto` option. Select a mode, press `Enter` and press the right arrow key to exit the options list, then select `Finish` to exit the configuration tool.

After you have finished modifying your audio settings, you need to restart your Raspberry Pi in order for your changes to take effect.



## If you're still not getting sound via HDMI

In some rare cases, it is necessary to edit `config.txt` to force HDMI mode (as opposed to DVI mode, which does not send sound). You can do this by editing `/boot/config.txt` and setting `hdmi_drive=2`, then rebooting for the change to take effect.
