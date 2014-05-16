# Installing XBMC on the Raspberry Pi

XBMC is media centre software which runs on Raspberry Pi.

![](images/openelec.png)

Two XBMC distributions are included in our easy Operating System installer [NOOBS](../installation/noobs.md): **OpenELEC** and **RaspBMC**.

## NOOBS

First, install NOOBS on an SD Card. Follow instructions on the [NOOBS](../installation/noobs.md) page.

With NOOBS on your SD Card, you should be able to boot the Raspberry Pi to the NOOBS Operating System selection screen:

![](../installation/images/noobs.png)

Select **OpenELEC** or **RaspBMC** and hit the `Install` button.

You'll be prompted to confirm  (this will delete any data on the SD card - so if you previously had Raspbian on it, be sure to back up your files first). If you're sure, click `Yes` to continue and the installation. This will take some time, and when complete will show a window saying:

```
OS(es) Installed Successfully
```

Click `OK` and your Pi will reboot in to the distribution you selected.

## Using XBMC

Now you've got your XBMC distribution installed, you can play media files, configure the system and install add-ons to do more.

You may be shown a Welcome screen which will help you configure your setup and help you get started.

![](images/openelec-main.png)

### Playing video files

You can copy video files on to your Pi's SD card or put them on a USB stick or external hard drive. To play these files, simply choose **VIDEOS** in the slider on the main screen, then **Files** and you should see your inserted media in the list of sources. Select your device and you should be able to navigate it like you would on a computer. Find the video file you wish to play, select it and it will play.

### Connecting a network drive

You can connect to a network device such as a NAS (Network Attached Storage) on your local network by using a wired connection. Connect your Raspberry Pi to your router with an ethernet cable. To connect to the device, select **VIDEOS** from the main screen and click **Add Videos...**.

The **Add Video source** screen will be shown. Hit **Browse** and choose the type of connection. For a NAS, choose **Windows network (SMB)** as it will be using the Samba protocol (an open source implementation of the Windows file share protocol). The device will show up if it can be found on the network. Add this device as a location and you'll be able to navigate its file system and play its media files.

### Settings

XBMC has a host of configurable options. You can change the screen resolution, choose a different skin, set up a screensaver, configure the file view, set localisation options, configure subtitles and much more. Just go to **SYSTEM** and **Settings** from the main screen.

### Add-ons

Add-ons provide extra functionality or enable connection to web services like YouTube.

The YouTube add-on showing search results:

![](images/xbmc-youtube.jpg)

You can configure add-ons from the settings menu. A selection is available for you to browse. Select one and you'll be prompted to install it. Each add-on has its own configurations.

## Control

You can use a keyboard and mouse with XBMC, or you can buy a TV remote with a USB receiver, or even use a presentation clicker with directional buttons.

You can also use an XBMC app on your smartphone (search for `XBMC` in your phone's app store), configure it to connect to your XBMC Pi's IP address and you can use the on-screen remote control or navigate the files from your phone and select what to play.
