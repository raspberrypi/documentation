# Raspberry Pi Display Troubleshooting

## Before You Start

### Have you got a good power supply?

Having intermittent problems, or seeing a little rainbow square in the top right corner? It is likely that you need a better power supply.

We recommend our official 2.5A adapter because we know it works, but any good 2.5A supply should work.

### Have you updated Raspberry Pi OS?

If not, many problems will be solved by making sure your software is up-to date.

You can undo any previous use of `rpi-update` and get your Pi back to the latest stable software by connecting
to a network and running:

```bash
sudo apt update
sudo apt install --reinstall libraspberrypi0 libraspberrypi-{bin,dev,doc} raspberrypi-bootloader
sudo reboot
```

## Frequent Problems

### My touchscreen doesn't work, or works intermittently

- Make sure you've updated Raspberry Pi OS (see above for steps)
- Check the smaller ribbon cable is seated properly

If you want to make sure your Pi has detected your touchscreen, try running:

```bash
dmesg | grep -i ft5406
```

You should see a couple of lines that look like this:

```text
[ 5.224267] rpi-ft5406 rpi_ft5406: Probing device
[ 5.225960] input: FT5406 memory based driver as /devices/virtual/input/input3
```

A detected touchscreen will also cause the `fbheight` and `fbwidth` parameters in `/proc/cmdline` to equal 480 and 800 respectively (the resolution of the screen). You can verify this by running:

```
cat /proc/cmdline | grep bcm2708_fb
```

### My screen is upside-down!

Depending on your display stand, you might find that the LCD display defaults to being upside-down. You can fix this by rotating it with `/boot/config.txt`.

```bash
sudo nano /boot/config.txt
```

Then add:

```bash
lcd_rotate=2
```

Hit `CTRL+X` and `y` to save. And finally:

```
sudo reboot
```

### My display fades out to weird patterns when I shutdown/reboot my Pi

Don't panic! This is perfectly normal.

### My display is black

* Make sure you've updated Raspberry Pi OS (see above for steps)
* Check the ribbon cable between your Pi and the LCD is properly seated
* Make sure you have a SD card properly inserted into your Pi

### My display is white

* Check the larger ribbon cable between the display and driver board is properly seated

### Raspberry Pi OS says my screen is 752x448. Surely that's wrong?

Yes, the screen should be 800x480. This is a result of overscan being enabled.

Disable it by running raspi-config:

```bash
sudo raspi-config
```

And then navigating to **Advanced Options** > **Overscan** and picking **Disable**. 

### My touchscreen isn't aligned correctly: my taps are slightly out

This is probably also a side-effect of overscan being enabled, try the solution above.

### My screen isn't working with my old Model B or Model A Pi

The Model A or B Pi need a couple of extra connections, and an extra line of config. Please see [the legacy display support page](legacy.md).

### Some windows are cut off at the bottom of the screen so I can't use them

If some windows in X are cut off at the side/bottom of the screen, this is unfortunately a side-effect of developers assuming a minimum screen resolution of 1024x768 pixels.

You can usually reveal hidden buttons and fields by;

- right clicking on the edge or top of the window,
- picking "move"
- using the up arrow key to nudge the window up off the top of the screen

If you don't have a mouse, see the right click fix below.

## Tips & Tricks

### How do I use multiple monitors?

At the moment you can't use HDMI and the LCD together in the X desktop, but you can send the output of certain applications to one screen or the other.

Omxplayer is one example. It has been modified to enable secondary display output.

To start displaying a video onto the LCD display (assuming it is the default display) just type:

```bash
omxplayer video.mkv
```

To start a second video onto the HDMI type:

```bash
omxplayer --display=5 video.mkv
```

**Please note: you may need to increase the amount of memory allocated to the GPU to 128MB if the videos are 1080P. Adjust the gpu_mem value in config.txt for this. The Raspberry Pi headline figures are 1080P30 decode, so if you are using two 1080P clips it may not play correctly depending on the complexity of the videos.**

Display numbers are:

* LCD: 4
* TV/HDMI: 5
* Auto select non-default display: 6

### How do I enable right click?

You can emulate a right click with a setting change. Just:

```bash
sudo nano /etc/X11/xorg.conf
```

Paste in:

```
Section "InputClass"
   Identifier "calibration"
   Driver "evdev"
   MatchProduct "FT5406 memory based driver"

   Option "EmulateThirdButton" "1"
   Option "EmulateThirdButtonTimeout" "750"
   Option "EmulateThirdButtonMoveThreshold" "30"
EndSection
```

Hit `CTRL+X` and `y` to save. Then:

```bash
sudo reboot
```

Once enabled, right click works by pressing and holding the touchscreen and will be activated after a short delay.

### How do I get an on-screen keyboard?

#### Florence Virtual Keyboard

Install with:

```bash
sudo apt install florence
```

#### Matchbox Virtual Keyboard

Install like so:

```bash
sudo apt install matchbox-keyboard
```

And then find in **Accessories** > **Keyboard**.

