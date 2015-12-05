# Installing Operating System Images on Mac OS

On Mac OS you have the choice of the command line `dd` tool or using the graphical tool ImageWriter to write the image to your SD card.

## (Mostly) graphical interface

- Connect the SD card reader with the SD card inside. Note that it must be formatted in FAT32.
- From the Apple menu, choose About This Mac, then click on More info...; if you are using Mac OS X 10.8.x Mountain Lion or newer then click on System Report.
- Click on USB (or Card Reader if using a built-in SD card reader) then search for your SD card in the upper right section of the window. Click on it, then search for the BSD name in the lower right section; it will look something like 'diskn' where n is a number (for example, disk4). Make sure you take a note of this number.
- Unmount the partition so that you will be allowed to overwrite the disk; to do this, open Disk Utility and unmount it (do not eject it, or you will have to reconnect it). Note that On Mac OS X 10.8.x Mountain Lion, "Verify Disk" (before unmounting) will display the BSD name as "/dev/disk1s1" or similar, allowing you to skip the previous two steps.
- From the terminal run:

    ```
    sudo dd bs=1m if=path_of_your_image.img of=/dev/rdiskn
    ```

    Remember to replace `n` with the number that you noted before!

   - If this command fails, try using `disk` instead of `rdisk`:
    
       ```
       sudo dd bs=1m if=path_of_your_image.img of=/dev/diskn
       ```

## Command line

- If you are comfortable with the command line, you can write the image to a SD card without any additional software. Open a terminal, then run:

    `diskutil list`

- Identify the disk (not partition) of your SD card e.g. `disk4` (not `disk4s1`).
- Unmount your SD card by using the disk identifier to prepare copying data to it:

    `diskutil unmountDisk /dev/disk<disk# from diskutil>`

    e.g. `diskutil unmountDisk /dev/disk4`
    
- Copy the data to your SD card:

    `sudo dd bs=1m if=image.img of=/dev/rdisk<disk# from diskutil>`

    e.g. `sudo dd bs=1m if=2015-11-21-raspbian-jessie.img of=/dev/rdisk4`

    - This may result in an ``dd: invalid number '1m'`` error if you have GNU
    coreutils installed. In that case you need to use ``1M``:

       `sudo dd bs=1M if=image.img of=/dev/rdisk<disk# from diskutil>`

    This will take a few minutes, depending on the image file size.
    You can check the progress by sending a `SIGINFO` signal pressing <kbd>Ctrl</kbd>+<kbd>T</kbd>.
    
    - If this command still fails, try using `disk` instead of `rdisk`:
    
       ```
       e.g. `sudo dd bs=1m if=2015-11-21-raspbian-jessie.img of=/dev/disk4`
       ```
       or
       ```
       e.g. `sudo dd bs=1M if=2015-11-21-raspbian-jessie.img of=/dev/disk4`
       ```

## Alternative method

**Note: Some users have reported issues with using Mac OS X to create SD cards.**

These commands and actions need to be performed from an account that has administrator privileges.

- From the terminal run `df -h`.
- Connect the SD card reader with the SD card inside.
- Run `df -h` again and look for the new device that wasn't listed last time. Record the device name of the filesystem's partition, for example `/dev/disk3s1`.
- Unmount the partition so that you will be allowed to overwrite the disk:

    ```
    sudo diskutil unmount /dev/disk3s1
    ```

    (or open Disk Utility and unmount the partition of the SD card (do not eject it, or you will have to reconnect it)
- Using the device name of the partition, work out the raw device name for the entire disk by omitting the final "s1" and replacing "disk" with "rdisk". This is very important as you will lose all data on the hard drive if you provide the wrong device name. Make sure the device name is the name of the whole SD card as described above, not just a partition of it (for example, rdisk3, not rdisk3s1). Similarly, you might have another SD drive name/number like rdisk2 or rdisk4; you can check again by using the `df -h` command both before and after you insert your SD card reader into your Mac. For example, `/dev/disk3s1` becomes `/dev/rdisk3`.
- In the terminal, write the image to the card with this command, using the raw disk device name from above. Read the above step carefully to be sure you use the correct rdisk number here:
    ```
    sudo dd bs=1m if=2015-11-21-raspbian-jessie.img of=/dev/rdisk3
    ```

    If the above command reports an error (`dd: bs: illegal numeric value`), please change `bs=1m` to `bs=1M`.

    If the above command reports an error `dd: /dev/rdisk3: Permission denied` then that is because the partition table of the SD card is being protected against being overwritten by MacOS. Erase the SD card's partition table using this command:
    ```
    sudo diskutil partitionDisk /dev/disk3 1 MBR "Free Space" "%noformat%" 100%
    ```
    That command will also set the permissions on the device to allow writing. Now try the `dd` command again.

    Note that `dd` will not feedback any information until there is an error or it is finished; information will be shown and the disk will re-mount when complete. However if you wish to view the progress you can use 'ctrl-T'; this generates SIGINFO, the status argument of your tty, and will display information on the process.
- After the `dd` command finishes, eject the card:

    ```
    sudo diskutil eject /dev/rdisk3
    ```

    (or: open Disk Utility and eject the SD card)

---

*This article uses content from the eLinux wiki page [RPi_Easy_SD_Card_Setup](http://elinux.org/RPi_Easy_SD_Card_Setup), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
