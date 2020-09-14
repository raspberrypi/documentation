# It's all booted, but the display is...wrong...

What is the actual problem?

- [No display at all?](#no-display-at-all)
- [The edges of the display are off screen?](#the-edges-of-the-display-are-off-screen)
- [Everything is HUGE?](#everything-is-huge)
- [The picture quality is bad?](#the-picture-quality-is-bad)
- [My Raspberry Pi 4 is not displaying 1366x768 correctly](#my-raspberry-pi-4-is-not-displaying-1366x768-correctly)

## No display at all?

If you don't get any output at all on your display device, first check that the HDMI cable is correctly plugged in. Then check that the display device is set to the correct input - some devices have two HDMI in ports, so you need to have the device set to the right one.

## The edges of the display are off screen?

If the display seems to overlap the display device, then it's likely that the display device has overscan enabled. This is an old system hangover from CRT days, but still present on some modern TV's. If you can find the settings on your TV to turn off overscan (it might be called something else), that is the best option, then ensure the Pi itself isn't comnpensating for the overscan. To do this, go to the desktop menu, select `Raspberry Pi Configuration`, then the `Display` tab, and disable the `overscan` option.

## Everything is HUGE!

On a small display, sometimes things can look rather large, or, on larger displays the pixel doubling option may have been enabled. To turn doubling on or off, go to the desktop menu, select `Raspberry Pi Configuration`, then the `Display` tab, and use the `Pixel Doubling` option.

## The picture quality is bad!

HDMI is a digital format, and on the whole works very well and gives great picture quality. However, very cheap cables made, it appears, out of wet string can cause quality issues. Always ensure you use a good quality cable; this is especially important at the higher 4K resolutions available on the Raspberry Pi 4.

## My Raspberry Pi 4 is not displaying 1366x768 correctly.

The Raspberry Pi 4 has updated the HDMI hardware to enable the twin output 4k modes. On the whole this makes no difference to the average user, but there is one caveat. If you display is 1366x768, that is not a mode that can be supported by the new hardware. The software will drop down to a lower resolution mode to cope, or in some cases might give a blank screen. See [here](../../configuration/config-txt/pi4-hdmi.md) for more details. 
