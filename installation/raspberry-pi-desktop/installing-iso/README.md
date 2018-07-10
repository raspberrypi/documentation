# Installing Raspberry Pi Desktop on a DVD or USB stick

Once the image file (which has the extension `.iso`) is downloaded, it needs to be be copied to the boot media, i.e. a DVD, USB stick or SD card.

## DVD

If using a DVD (note, a CD does not have enough capcacity for the current image), then you will need to use DVD burning software to copy the ISO image to it. On Linux, the Brassero application can do this, or if using Ubuntu or a derivative, you can use the `Startup disk creator` application. Both these are self explanatory. Windows (since Windows 7) has a built in image burning tool. Right click in the ISO image file and select the burn option.

## USB stick or SD card

To install the image on an USB stick, you use a similar procedure to burning a SD card for use on a Raspberry Pi. See our [installing images guide](../../installing-images/README.md). You can download [Etcher](https://etcher.io/). Run it, select the ISO image file, and the destination device (your USB or SD card), and click the Flash button. Alternatively, Linux and Mac users can use the `dd` command.

Burning an images can take quite a few minutes.
