# My Raspberry Pi won't work - help!

Let's go through some simple steps to find out what is going on.

## Blinky blinky lights

The first thing to look at is the little LED lights on your Pi. Watch what happens after you plug the power into the Pi - do you see a light come on? Does one of the lights flash in an irregular way, or is there a pattern?

### Nothing lights up at all on my Pi

Your Pi is not getting enough power, or it's just broken.

We recommend using our official Raspberry Pi Power Supply: for Pi 4 you need the [USB-C version](https://www.raspberrypi.org/products/type-c-power-supply/), all other models use the [micro USB version](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/).

All Raspberry Pis are tested before they leave the factory, but it is possible that it got broken somehow before you plugged it in. 

**Raspberry Pi Zero:** there's two micro USB connectors on this model - make sure you plug the power into the one on the left labelled `PWR`.

### I see irregular blinks

Good stuff: this means your Pi *is* starting up but is having difficulty talking to your screen: see our [display troubleshooting section](./display.md).

### The blinks seem to have a pattern

This means the Pi is having difficulty starting up: the pattern of the blinks indicates the exact problem.

*3 flashes* or  
*4 flashes*  
There something wrong with your SD card: perhaps it has not been imaged correctly?

*7 flashes*  
Your Pi has started to boot, but the operating system cannot be loaded. Again, this probably means a badly imaged SD card.

*8 flashes*  
This is caused by an out-of-date SD card image. Use [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to image your SD card with the latest version.

All of these problems could also be caused by the Pi not receiving enough power. We recommend using our official Raspberry Pi Power Supply: for Pi 4 you need the [USB-C version](https://www.raspberrypi.org/products/type-c-power-supply/), all other models use the [micro USB version](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/).

## I see something in the display, but it's not what I was expecting!

### I've got a rainbow screen

This is usually caused by an out-of-date SD card image. Use [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to image your SD card with the latest version.

### There's a lightning bolt in the top left corner

This means that your Raspberry Pi has detecting that it is not getting enough power. We recommend using our official Raspberry Pi Power Supply: for Pi 4 you need the [USB-C version](https://www.raspberrypi.org/products/type-c-power-supply/), all other models use the [micro USB version](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/).
