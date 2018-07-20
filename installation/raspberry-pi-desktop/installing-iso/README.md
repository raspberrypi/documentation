# Installing Raspberry Pi Desktop on a DVD or USB stick

Once the image file (which has the extension `.iso`) is downloaded, it needs to be be copied to a boot medium, i.e. a DVD, USB stick, or SD card.

## DVD

If you are using a DVD (note: a CD does not have enough capcacity for the current image), then you will need to use DVD burning software to copy the ISO image to it. On Linux, the Brassero application can do this, or if you are using Ubuntu or a derivative, you can use the **Startup disk creator** application. Both these applications are self-explanatory. Windows (since Windows 7) has a built-in image burning tool. Right-click in the ISO image file and select the **Burn** option.

## USB stick or SD card

To install the image on an USB stick, you use a similar procedure to burning a SD card for use with a Raspberry Pi — see our ['Installing images' guide](../../installing-images/README.md) for help. You can download Etcher from [here](https://etcher.io/). Run it, select the ISO image file and the destination device (your USB or SD card), and click the **Flash** button. Alternatively, Linux and Mac users can use the `dd` command.

Burning an image can take quite a few minutes.
