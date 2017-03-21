# Installing operating system images

This resource explains how to install a Raspberry Pi operating system image on an SD card. You will need another computer with an SD card reader to install the image.

We recommend most users download [NOOBS](../noobs.md), which is designed to be very easy to use. However, more advanced users looking to install a particular image should use this guide.

## Download the image

Official images for recommended operating systems are available to download from the Raspberry Pi website [Downloads page](https://www.raspberrypi.org/downloads/).

Alternative distributions are available from third-party vendors.

After downloading the `.zip` file, unzip it to get the image file (`.img`) for writing to your SD card.

Note: the Raspbian with PIXEL image contained in the ZIP archive is over 4GB in size and uses the [ZIP64](https://en.wikipedia.org/wiki/Zip_(file_format)#ZIP64) format. To uncompress the archive, a unzip tool that supports ZIP64 is required. The following zip tools support ZIP64:

- [7-Zip](http://www.7-zip.org/) (Windows)
- [The Unarchiver](http://unarchiver.c3.cx/unarchiver) (Mac)
- [Unzip](http://www.info-zip.org/mans/unzip.html) (Linux)

## Writing an image to the SD card

With the image file of the distribution of your choice, you need to use an image writing tool to install it on your SD card.

See our guide for your system:

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)
