# Installing operating system images using Windows

[Etcher](README.md) is typically the easiest option for most users to write images to SD cards, so it is a good place to start. If you're looking for an alternative on Windows, you can use `Win32DiskImager`:

## Win32DiskImager

- Insert the SD card into your SD card reader. You can use the SD card slot if you have one, or an SD adapter in a USB port. Note the drive letter assigned to the SD card. You can see the drive letter in the left hand column of Windows Explorer, for example **G:**
- Download the Win32DiskImager utility from the [Sourceforge Project page](http://sourceforge.net/projects/win32diskimager/) as an installer file, and run it to install the software.
- Run the `Win32DiskImager` utility from your desktop or menu.
- Select the image file you extracted earlier.
- In the device box, select the drive letter of the SD card. Be careful to select the correct drive: if you choose the wrong drive you could destroy the data on your computer's hard disk! If you are using an SD card slot in your computer, and can't see the drive in the Win32DiskImager window, try using an external SD adapter.
- Click 'Write' and wait for the write to complete.
- Exit the imager and eject the SD card.

---

*This article uses content from the eLinux wiki page [RPi_Easy_SD_Card_Setup](http://elinux.org/RPi_Easy_SD_Card_Setup), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
