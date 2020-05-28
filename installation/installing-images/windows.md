# Installing operating system images using Windows

[Raspberry Pi Imager](README.md) is our recommended option for most users to write images to SD cards, so it is a good place to start. If you're looking for an alternative on Windows, you can use balenaEtcher, Win32DiskImager or imgFlasher.

## balenaEtcher

- Download the Windows installer from [balena.io](https://www.balena.io/etcher/)
- Run balenaEtcher and select the unzipped Raspberry Pi OS image file
- Select the SD card drive
- Finally, click **Burn** to write the Raspberry Pi OS image to the SD card
- You'll see a progress bar. Once complete, the utility will automatically unmount the SD card so it's safe to remove it from your computer.

## Win32DiskImager

- Insert the SD card into your SD card reader. You can use the SD card slot if you have one, or an SD adapter in a USB port. Note the drive letter assigned to the SD card. You can see the drive letter in the left hand column of Windows Explorer, for example **G:**
- Download the Win32DiskImager utility from the [Sourceforge Project page](http://sourceforge.net/projects/win32diskimager/) as an installer file, and run it to install the software.
- Run the `Win32DiskImager` utility from your desktop or menu.
- Select the image file you extracted earlier.
- In the device box, select the drive letter of the SD card. Be careful to select the correct drive: if you choose the wrong drive you could destroy the data on your computer's hard disk! If you are using an SD card slot in your computer, and can't see the drive in the Win32DiskImager window, try using an external SD adapter.
- Click 'Write' and wait for the write to complete.
- Exit the imager and eject the SD card.

## Upswift imgFlasher

- Download portable Windows version from [upswift.io](https://www.upswift.io/imgflasher/)
- Run imgFlasher and choose an image or zip file
- Choose SD card or USB drive
- Click on 'Flash'
- Wait until the flash is completed.

---

*This article uses content from the eLinux wiki page [RPi_Easy_SD_Card_Setup](http://elinux.org/RPi_Easy_SD_Card_Setup), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
