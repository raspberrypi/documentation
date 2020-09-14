# My desktop isn't right...

The Raspberry Pi Desktop ios a modification of the well known LXDE desktop. We have made some changes to make it easier to use, and also fixed some bugs. But things can still not qork quite how you expect.

What is the actual problem?

- [I don't even have a desktop!](#no-display-at-all)
- [Edges are off the screen](#edges-are-off-the-screen)

## I don't have a desktop!

Have you installed the Raspberry Pi OS Lite? Have you booted in to console mode? 

### Raspberry Pi OS Lite

The lite version of our OS does not come with an installed desktop, so will always boot to a console until you install a desktop. You can install our desktop in to Lite using the following instructions.

```
sudo apt update
sudo apt full-upgrade
sudo apt install raspberrypi-ui-mods
sudo reboot
```

### Console mode

This is Linux's command line interface. It's very powerful, but a bit more difficult to use than our desktop. It's well worth learning, but you can practice that from within the desktop by using a terminal window.

If you actually have a desktop installed, then you can start it from the console, by typing:      

`startx`

If you want to get your machine to boot straight to the desktop instead of the console, try the following:

`sudo raspi-config`

Select `Boot options`, then the options to select `Desktop/CLI`. You probably want to select `Desktop Autologin`, which when you next boot will take you straight in to the desktop.


## Edges are off the screen

This usually means either the display or the Pi have overscan enabled. Try [this page](./display.md) for display issues.
