# Onboard analogue audio options in config.txt (3.5mm jack)

The onboard audio output uses config options to change the way the analogue audio is driven, and whether some firmware features are enabled or not.

## disable_audio_dither

By default, a 1.0LSB dither is applied to the audio stream if it is routed to the analogue audio output. This can create audible background "hiss" in some situations, for example when the ALSA volume is set to a low level. Set `disable_audio_dither` to `1` to disable dither application.

## enable_audio_dither

Audio dither (see disable_audio_dither above) is normally disabled when the audio samples are larger than 16 bits. Set this option to `1` to force the use of dithering for all bit depths.

## pwm_sample_bits

The `pwm_sample_bits` command adjusts the bit depth of the analogue audio output. The default bit depth is `11`. Selecting bit depths below `8` will result in nonfunctional audio, as settings below `8` result in a PLL frequency too low to support. This is generally only useful as a demonstration of how bit depth affects quantisation noise.




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
