# Installing operating system images

This resource explains how to install a Raspberry Pi operating system image on an SD card. You will need another computer with an SD card reader to install the image.

Before you start, don't forget to check [the SD card requirements](../sd-cards.md).

## Using Raspberry Pi Imager

Raspberry Pi have developed a graphical SD card writing tool that works on Mac OS, Ubuntu 18.04 and Windows, and is the easiest option for most users as it will download the image and install it automatically to the SD card.

- Download the latest version of [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) and install it.
- Connect an SD card reader with the SD card inside.
- Open Raspberry Pi Imager and choose the required OS from the list presented.
- Choose  the SD card you wish to write your image to.
- Review your selections and click 'WRITE' to begin writing data to the SD card.

## Using other tools

Most other tools require you to download the image first, then use the tool to write it to your SD card.

### Download the image

Official images for recommended operating systems are available to download from the Raspberry Pi website [downloads page](https://www.raspberrypi.org/downloads/).

Alternative distributions are available from third-party vendors.

You may need to unzip `.zip` downloads to get the image file (`.img`) to write to your SD card.

**Note**: the Raspbian with Raspberry Pi Desktop image contained in the ZIP archive is over 4GB in size and uses the [ZIP64](https://en.wikipedia.org/wiki/Zip_%28file_format%29#ZIP64) format. To uncompress the archive, a unzip tool that supports ZIP64 is required. The following zip tools support ZIP64:

- [7-Zip](http://www.7-zip.org/) (Windows)
- [The Unarchiver](http://unarchiver.c3.cx/unarchiver) (Mac)
- [Unzip](https://linux.die.net/man/1/unzip) (Linux)

### Writing the image

How you write the image to the SD card will depend on the operating system you are using. 

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)
- [Chrome OS](chromeos.md)
