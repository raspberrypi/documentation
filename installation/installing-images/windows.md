# Installing operating system images using Windows

- Insert the SD card into your SD card reader and check which drive letter was assigned. You can easily see the drive letter, such as `G:`, by looking in the left column of Windows Explorer. You can use the SD card slot if you have one, or a cheap SD adapter in a USB port.
- Download the Win32DiskImager utility from the [Sourceforge Project page](http://sourceforge.net/projects/win32diskimager/) as a zip file; you can run this from a USB drive.
- Extract the executable from the zip file and run the `Win32DiskImager` utility; you may need to run this as administrator. Right-click on the file, and select **Run as administrator**.
- Select the image file you extracted earlier.
- Select the drive letter of the SD card in the device box. Be careful to select the correct drive; if you get the wrong one you can destroy the data on your computer's hard disk! If you are using an SD card slot in your computer and can't see the drive in the Win32DiskImager window, try using an external SD adapter.
- Click `Write` and wait for the write to complete.
- Exit the imager and eject the SD card.

---

*This article uses content from the eLinux wiki page [RPi_Easy_SD_Card_Setup](http://elinux.org/RPi_Easy_SD_Card_Setup), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
