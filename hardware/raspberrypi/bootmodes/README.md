# IMPORTANT
This is preliminary information used by the beta testers for the development of the bootcode for mass storage and ethernet boot, but it is currently incorrect and not working.  If you'd like to join the beta test then please send your email to @gsholling on Twitter and I'll invite you to the Slack channel which we're using to discuss this...


# Raspberry Pi boot modes

## Introduction

The Raspberry Pi has a number of different stages of booting. This document is meant to help explain how the boot modes work, and which ones are supported for Linux booting.

* [Bootflow](bootflow.md) Boot sequence description
* [SD card](sdcard.md) SD card boot description
* [USB](usb.md) USB boot description
  * [Device boot](device.md) Booting as a mass storage device
  * [Host boot](host.md) Booting as a USB host
    * [Mass storage boot](msd.md) Boot from Mass Storage Device (MSD)
    * [Network boot](net.md) Boot from ethernet

