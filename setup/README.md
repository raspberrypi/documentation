# Setup

A guide to setting up your Raspberry Pi

## What you will need

### Essential (for general use)

- [SD card](../installation/sd-cards.md)
    - We recommend a minimum of 8GB class 4 or class 10 microSD card. To save time, you can get a card that is pre-installed with [NOOBS](../installation/noobs.md) or [Raspberry Pi OS](../installation/installing-images/README.md), although setting up your own card is easy.
- [Display and connectivity cable](monitor-connection.md)
    - Any HDMI/DVI monitor or TV should work as a display for the Pi. For best results, use a display with HDMI input; other types of connection for older devices are also available.
- Keyboard and mouse
    - Any standard USB keyboard and mouse will work with your Raspberry Pi.
    - Wireless keyboards and mice will work if already paired.
    - For keyboard layout configuration options see [raspi-config](../configuration/raspi-config.md).
- [Power supply](../hardware/raspberrypi/power/README.md)
    - The Pi is powered by a USB Micro [models pre 4B] or USB Type-C [model 4B] power supply (like most standard mobile phone chargers).
    - You need a good-quality power supply that can supply at least 3A at 5V for the Model 4B, 2A at 5V for the Model 3B and 3B+, or 700mA at 5V for the earlier, lower-powered Pi models. We recommend using the [official Raspberry Pi power supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/), which is designed specifically for Raspberry Pi.
    - Low-current (~700mA) power supplies will work for basic usage, but are likely to cause the Pi to reboot if it draws too much power. They are not suitable for use with the Pi 3 or 4.

### Optional

- Ethernet (network) cable [Model B/B+/2B/3B/3B+/4B only]
    - An Ethernet cable is used to connect your Pi to a local network and the internet.
- [USB wireless dongle](../configuration/wireless/README.md)
    - Only required if you need wireless connectivity and are using an older model without built-in wireless functionality.
- Audio lead
    - Audio can be played through speakers or headphones using a standard 3.5mm jack.
    - Without an HDMI cable, an audio lead is necessary to produce sound.
    - No separate audio lead is necessary if you're using an HDMI cable to connect to a monitor with speakers, as audio can be played directly through the display; but it is possible to connect one if you prefer to have the audio played through other speakers - this requires [configuration](../configuration/audio-config.md).

## Troubleshooting

For any issues during setup, search [the forums](https://www.raspberrypi.org/forums/) for a solution. If you cannot find one, please post your problem, providing as much detail as possible.
