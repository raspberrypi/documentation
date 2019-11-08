# Installing operating system images

This resource explains how to install a Raspberry Pi operating system image on an SD card. You will need another computer with an SD card reader to install the image.

We recommend most users download [NOOBS](../noobs.md), which is designed to be very easy to use. However, more advanced users looking to install a particular image should use this guide.

## Download the image

Official images for recommended operating systems are available to download from the Raspberry Pi website [Downloads page](https://www.raspberrypi.org/downloads/).

Alternative distributions are available from third-party vendors.

If you're not using balenaEtcher (see below), you'll need to unzip `.zip` downloads to get the image file (`.img`) to write to your SD card.

**Note**: the Raspbian with Raspberry Pi Desktop image contained in the ZIP archive is over 4GB in size and uses the [ZIP64](https://en.wikipedia.org/wiki/Zip_%28file_format%29#ZIP64) format. To uncompress the archive, a unzip tool that supports ZIP64 is required. The following zip tools support ZIP64:

- [7-Zip](http://www.7-zip.org/) (Windows)
- [The Unarchiver](http://unarchiver.c3.cx/unarchiver) (Mac)
- [Unzip](https://linux.die.net/man/1/unzip) (Linux)

## Writing an image to the SD card

Before you start, don't forget to check [the SD card requirements](../sd-cards.md).

You will need to use an image writing tool to install the image you have downloaded on your SD card.

**balenaEtcher** is a graphical SD card writing tool that works on Mac OS, Linux and Windows, and is the easiest option for most users. balenaEtcher also supports writing images directly from the zip file, without any unzipping required. To write your image with balenaEtcher:

- Download the latest version of [balenaEtcher](https://www.balena.io/etcher/) and install it.
- Connect an SD card reader with the SD card inside.
- Open balenaEtcher and select from your hard drive the Raspberry Pi `.img` or `.zip` file you wish to write to the SD card.
- Select the SD card you wish to write your image to.
- Review your selections and click 'Flash!' to begin writing data to the SD card.

**Note**: for Linux users, `zenity` might need to be installed on your machine for `balenaEtcher` to be able to write the image on your SD card.

For more advanced control of this process, see our system-specific guides:

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)
- [Chrome OS](chromeos.md)
