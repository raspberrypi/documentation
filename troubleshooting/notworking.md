# My Raspberry Pi won't work - help!

Let's go through some simple steps to find out what is going on.

## Blinky blinky lights

The first thing to look at is the little LED lights on your Pi. Watch what happens after you plug the power into the Pi - do you see a light come on? Does one of the lights flash in an irregular way, or is there a pattern?

### Nothing lights up at all on my Pi

Your Pi is not getting enough power, or it's just broken. All Raspberry Pis are tested before they leave the factory, but it is possible that it got broken somehow before you plugged it in.

### I see irregular blinks

Good stuff: this means your Pi is starting up. It just needs to get the display working on your screen.

### The blinks seem to have a pattern

This means the Pi is having difficulty starting up. The pattern of the blinks indicates the exact problem.

*3 flashes* or  
*4 flashes*  
There something wrong with your SD card: perhaps it has not been imaged correctly?

*7 flashes*  
Your Pi has started to boot, but the operating system cannot be loaded. Again, this probably means a badly imaged SD card.

*8 flashes*  
This is caused by an out-of-date SD card image. Use [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to image your SD card with the latest version.





All of these problems could be caused by the Pi not receiving enough power. We recommend using our official Raspberry Pi Power Supply: for Pi 4 you need the [USB-C version](https://www.raspberrypi.org/products/type-c-power-supply/), all other models use the [micro USB version](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/).


#### jamesh65 content below.

OK, you have imaged your SD card, plugged it in, plugged in a monitor or TV, plugged in the power. But nothing happens. What's going on?

First thing to know is that all Pi devices are tested prior to leaving the factory, so they worked at that point. It's technically possible for it to be damaged in transit, or to fail on its first boot, but in the huge majority of cases, boot problems are caused by a defective or badly imaged SD card.

- [Nothing at all is happening!](#nothing-at-all-is-happening)
- [I get a pretty rainbow like screen, but nothing then happens](#i-get-a-pretty-rainbow-like-screen-but-nothing-then-happens)
- [I've got the rainbow screen, and a lightning bolt icon on the top right](#ive-got-the-rainbow-screen-and-a-lightning-bolt-icon-on-the-top-right)


## Nothing at all is happening!

### I can see ACT LED flashing on the board.

OK, so it's got power. Are the flashes [regular](#regular), or seemingly [random](#irregular)?

#### Regular

So, if you get a regular repeating pattern, then the Pi is trying to boot but there is something wrong

*3 flashes* start.elf not found.  
*4 flashes* start.elf corrupt.  
There something wrong with your SD card, perhaps it has not been imaged correctly.

*7 flashes* kernel.img not found.  
The device has started to boot, but the Operating system image cannot be loaded for some reason. Again, this probably means a badly imaged SD card.

*8 flashes* SDRAM not recognised.

See [here](#i-appear-to-have-the-wrong-version-of-something) for how to update.

#### Irregular

OK, lots of irregular flashes over 20s or so means the device is booting up. If you are not getting any display, then you need to check out the [display troubleshooting section](./display.md)

### No LED's turned on

This means that the device is not getting power, or is completely broken. In the case of the Zero, its can also mean that it's been unable to load the start.elf firmware, in which case, [re-image](#i-appear-to-have-the-wrong-version-of-something) the SD card with the latest Raspbian release. 

#### Is the power supply is plugged in to the mains and the correct input on the Raspberry Pi?

Make sure when using the Pi Zero that you are using the power in connector.

##### Yes, still nothing.

Does the power supply meets the minimum specification? We recommend the official power supply for all Raspberry Pi devices. 
Have you an alternative power supply you can try, or if the USB lead is detachable, a different, good quality, lead?

## I get a pretty rainbow like screen, but nothing then happens

The firmware has loaded, detected the display and displayed a splash screen, but has now stalled for some reason. This is almost certainly the wrong version of firmware or kernel on the SD card. [Update it](#i-appear-to-have-the-wrong-version-of-something)

## I've got the rainbow screen, and a lightning bolt icon on the top right

The firmware on the SD card is too old to support the Model 3B/3B+ you are using. [Update it](#i-appear-to-have-the-wrong-version-of-something)


## I appear to have the wrong version of something

You will need to upgrade the version of firmware/OS kernel.

You can reimage the SD card completely with the latest Raspbian release, but this will erase all user data on the SD card. 

If you have an older Pi device that already works with the SD card, you can upgrade without re-imaging by booting to the command line and using 
```
sudo apt update
sudo apt full-upgrade
```

Note that this cannot upgrade major OS revisions, so if your SD card installation is quite old it might be easier to re-image it or try a new SD card with the latest OS installed.
