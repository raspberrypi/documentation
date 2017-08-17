# Installing operating system images on Mac OS

[Etcher](README.md) is typically the easiest option for most users to write images to SD cards, so it is a good place to start. If you're looking for more advanced options on Mac OS, you can use the built-in graphical and command line tools below.

**Note**: use of the `dd` tool can overwrite any partition of your machine. If you specify the wrong device in the instructions below, you could delete your primary Mac OS partition. Please be careful.

## (Mostly) graphical interface

- Connect the SD card reader with the SD card inside. Note that it must be formatted as FAT32.
- From the Apple menu, choose 'About This Mac', then click on 'More info...'. If you are using Mac OS X 10.8.x Mountain Lion or newer, you will then need to click on 'System Report'.
- Click on 'USB' (or 'Card Reader' if you are using a built-in SD card reader), then search for your SD card in the upper right section of the window. Click on it, then search for the BSD name in the lower right section. It will look something like `diskn` where `n` is a number (for example, `disk4`). Make sure you take a note of this number.
- Unmount the partition so that you will be allowed to overwrite the disk. To do this, open Disk Utility and unmount it. Do not eject it. If you eject it, you will have to reconnect it. Note that on Mac OS X 10.8.x Mountain Lion, 'Verify Disk' (before unmounting) will display the BSD name as `/dev/disk1s2` or similar, allowing you to skip the previous two steps. Note down the number that appears after 'disk', in this case the number '1'.
- From the terminal, run the following command:

    ```
    sudo dd bs=1m if=path_of_your_image.img of=/dev/rdiskn conv=sync
    ```

    Remember to replace `n` with the number that you noted before!
    
    This will take a few minutes, depending on the image file size. You can check the progress by sending a SIGINFO signal                  (press Ctrl+T).


    - If this command fails, try using `disk` instead of `rdisk`:
    
       ```
       sudo dd bs=1m if=path_of_your_image.img of=/dev/diskn conv=sync
       ```
This will take a few minutes, depending on the size of the image file. To check the progress, open Activity Monitor, click the Disk tab and find the process with the name `dd`. If `dd` is not in the list, you may need to select 'All Processes' from the View menu. The Bytes Read column will display the amount of data that has been read from the image. Compare that to the file size of the image to determine progress.


## Command line

- If you are comfortable with the command line, you can write the image to an SD card without any additional software. Open a terminal, then run:

    `diskutil list`

- Identify the disk (not the partition) of your SD card, e.g. `disk4`, not `disk4s1`.
- Unmount your SD card by using the disk identifier, to prepare it for copying data:

    `diskutil unmountDisk /dev/disk<disk# from diskutil>`

    where `disk` is your BSD name e.g. `diskutil unmountDisk /dev/disk4`
    
- Copy the data to your SD card:

    `sudo dd bs=1m if=image.img of=/dev/rdisk<disk# from diskutil> conv=sync`

    where `disk` is your BSD name e.g. `sudo dd bs=1m if=2017-08-16-raspbian-jessie.img of=/dev/rdisk4 conv=sync`

    - This may result in a ``dd: invalid number '1m'`` error if you have GNU
    coreutils installed. In that case, you need to use a block size of `1M` in the `bs=` section, as follows:

       `sudo dd bs=1M if=image.img of=/dev/rdisk<disk# from diskutil> conv=sync`

    This will take a few minutes, depending on the image file size. You can check the progress by sending a `SIGINFO` signal (press Ctrl+T).
    
    - If this command still fails, try using `disk` instead of `rdisk`, for example:
    
       ```
       sudo dd bs=1m if=2017-08-16-raspbian-jessie.img of=/dev/disk4 conv=sync
       ```
       or
       ```
       sudo dd bs=1M if=2017-08-16-raspbian-jessie.img of=/dev/disk4 conv=sync
       ```

## Alternative method

**Note**: some users have reported issues with using this method to create SD cards.

These commands and actions must be performed from an account that has administrator privileges.

- From the terminal run `df -h`.
- Connect the SD card reader with the SD card inside.
- Run `df -h` again and look for the new device that was not previously listed. Record the device name of the filesystem's partition, for example `/dev/disk3s1`.
- Unmount the partition so that you will be allowed to overwrite the disk:

    ```
    sudo diskutil unmount /dev/disk3s1
    ```

    Alternatively, open Disk Utility and unmount the partition of the SD card. Do not eject it. If you eject it, you will have to reconnect it.
- Using the device name of the partition, work out the **raw device name** for the entire disk by omitting the final `s1` and replacing `disk` with `rdisk`. This is very important, as you will lose all data on the hard drive if you provide the wrong device name. Make sure the device name is the name of the whole SD card as described above, not just a partition of it, for example, `rdisk3`, not `rdisk3s1`. Similarly, you might have another SD drive name/number like `rdisk2` or `rdisk4`. You can check again by using the `df -h` command, both before and after you insert your SD card reader into your Mac. For example: `/dev/disk3s1` becomes `/dev/rdisk3`.
- In the terminal, write the image to the card with this command, using the raw device name from above. Read the above step carefully to make sure that you use the correct `rdisk` number here:
    
    ```
    sudo dd bs=1m if=2017-08-16-raspbian-jessie.img of=/dev/rdisk3 conv=sync
    ```

    If the above command reports the error `dd: bs: illegal numeric value`, change the block size `bs=1m` to `bs=1M`.

    If the above command reports the error `dd: /dev/rdisk3: Permission denied`, the partition table of the SD card is being protected against being overwritten by Mac OS. Erase the SD card's partition table using this command:
    
    ```
    sudo diskutil partitionDisk /dev/disk3 1 MBR "Free Space" "%noformat%" 100%
    ```
    
    That command will also set the permissions on the device to allow writing. Now try the `dd` command again.

    Note that `dd` will not provide any on-screen information until there is an error, or it is finished. When the process is complete, information will be shown and the disk will re-mount. If you wish to view the progress, you can use Ctrl-T. This generates SIGINFO, the status argument of your terminal, and will display information on the process.
- After the `dd` command finishes, eject the card:

    ```
    sudo diskutil eject /dev/rdisk3
    ```

    Alternatively, open Disk Utility and use this to eject the SD card.

---

*This article uses content from the eLinux wiki page [RPi_Easy_SD_Card_Setup](http://elinux.org/RPi_Easy_SD_Card_Setup), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
