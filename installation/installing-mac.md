# Installing Operating System Images on Mac OS

On Mac OS you have the choice of the command line `dd` tool or using the graphical tool ImageWriter to write the image to your SD card.

## (Mostly) Graphical interface

- Connect the SD card reader with the SD card inside; note: must be formatted in FAT32

- From the Apple menu, choose About This Mac, then click on More info...; if you are using Mac OS X 10.8.x Mountain Lion then click on System report.

- Click on USB (or Card Reader if using an in-built SD card reader) then search for your SD card in the upper right section of the window; click it, then search for BSD name in the lower right section: must be something like diskn where n is a number (for example, disk4). Note this number

- Unmount the partition so that you will be allowed to overwrite the disk by opening Disk Utility and unmounting it (do not eject it, or you have to reconnect it). Note: On Mac OS X 10.8.x Mountain Lion, "Verify Disk" (before unmounting) will display the BSD name as "/dev/disk1s1" (or similar), allowing you to skip the previous two steps.

- From the Terminal run:
    - `sudo dd if=path_of_your_image.img of=/dev/diskn bs=4m`
    - Remember to replace `n` with the number that you noted before!

## Command line

- If you are comfortable with the command line, you can image a card without any additional software. Run:

    `diskutil list`

- Identify the disk (not partition) of your SD card. e.g. `disk4` (not `disk4s1`)

    `diskutil unmountDisk /dev/<disk# from diskutil>`

    e.g. `diskutil unmountDisk /dev/disk4`

    `sudo dd bs=1m if=image.img of=/dev/DISK`

    e.g. `sudo dd bs=1m if=2014-01-07-wheezy-raspbian.img of=/dev/disk4`

    (This will take a few minutes)

**Alternatively:**

Note: Some users have reported issues with using Mac OS X to create SD cards.

These commands and actions need to be performed from an account that has administrator privileges.

- From the terminal run `df -h`

- Connect the SD card reader with the SD card inside

- Run `df -h` again and look for the new device that wasn't listed last time. Record the device name of the filesystem's partition, for example, `/dev/disk3s1`

- Unmount the partition so that you will be allowed to overwrite the disk:

    ```
    sudo diskutil unmount /dev/disk3s1
    ```

    (or: open Disk Utility and unmount the partition of the SD card (do not eject it, or you have to reconnect it)

- Using the device name of the partition work out the raw device name for the entire disk, by omitting the final "s1" and replacing "disk" with "rdisk" (this is very important: you will lose all data on the hard drive on your computer if you get the wrong device name). Make sure the device name is the name of the whole SD card as described above, not just a partition of it (for example, rdisk3, not rdisk3s1. Similarly you might have another SD drive name/number like rdisk2 or rdisk4, etc. -- recheck by using the df -h command both before & after you insert your SD card reader into your Mac if you have any doubts!):

    For example, `/dev/disk3s1` => `/dev/rdisk3`

- In the terminal write the image to the card with this command, using the raw disk device name from above (read carefully the above step, to be sure you use the correct rdisk# here!):

    `sudo dd bs=1m if=2014-01-07-wheezy-raspbian/2014-01-07-wheezy-raspbian.img of=/dev/rdisk3`

    If the above command report an error (`dd: bs: illegal numeric value`), please change `bs=1M` to `bs=1m`

    (note that dd will not feedback any information until there is an error or it is finished, information will show and disk will re-mount when complete. However if you are curious as to the progresss - ctrl-T (SIGINFO, the status argument of your tty) will display some en-route statistics).

- After the dd command finishes, eject the card:

    ```
    sudo diskutil eject /dev/rdisk3
    ```

    (or: open Disk Utility and eject the SD card)
