# Installing operating system images

This resource explains how to install a Raspberry Pi operating system image on an SD card. You will need another computer with an SD card reader to install the image.

We recommend most users download [NOOBS](../noobs.md), which is designed to be very easy to use. However, more advanced users looking to install a particular image should use this guide.

## Download the image

Official images for recommended operating systems are available to download from the Raspberry Pi website [Downloads page](https://www.raspberrypi.org/downloads/).

Alternative distributions are available from third-party vendors.

If you're not using Etcher (see below), you'll need to unzip `.zip` downloads to get the image file (`.img`) to write to your SD card.

**Note**: the Raspbian with PIXEL image contained in the ZIP archive is over 4GB in size and uses the [ZIP64](https://en.wikipedia.org/wiki/Zip_(file_format)#ZIP64) format. To uncompress the archive, a unzip tool that supports ZIP64 is required. The following zip tools support ZIP64:

- [7-Zip](http://www.7-zip.org/) (Windows)
- [The Unarchiver](http://unarchiver.c3.cx/unarchiver) (Mac)
- [Unzip](http://www.info-zip.org/mans/unzip.html) (Linux)

## Writing an image to the SD card

You will need to use an image writing tool to install the image you have downloaded on your SD card.

**Etcher** is a graphical SD card writing tool that works on Mac OS, Linux and Windows, and is the easiest option for most users. Etcher also supports writing images directly from the zip file, without any unzipping required. To write your image with Etcher:

- Download [Etcher](https://etcher.io/) and install it.
- Connect an SD card reader with the SD card inside.
- Open Etcher and select from your hard drive the Raspberry Pi `.img` or `.zip` file you wish to write to the SD card.
- Select the SD card you wish to write your image to.
- Review your selections and click 'Flash!' to begin writing data to the SD card.

For more advanced control of this process, see our system-specific guides:

- [Linux](linux.md)
- [Mac OS](mac.md)
- [Windows](windows.md)
