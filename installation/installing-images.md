# Installing Operating System Images

How to install a Raspberry Pi Operating System image on an SD card

Note: this guide is for advanced users wanting to install a specific OS image to an SD card. Beginners are adviced to use the easy installer tool [NOOBS](https://github.com/raspberrypi/documentation/blob/master/installation/noobs.md)

## Download the image

Official images for recommended Operating Systems are available to download from the Raspberry Pi website: [raspberrypi.org/downloads](http://www.raspberrypi.org/downloads/)

Alternative distributions are available from third party vendors

## Writing an image to the SD card

With the image file of the distribution of your choice, you need to use an image writing tool to install it on your SD card

### Windows

- Insert the SD card into your SD card reader and check which drive letter was assigned. You can easily see the drive letter (for example G:) by looking in the left column of Windows Explorer. You can use the SD Card slot (if you have one) or a cheap Adapter in a USB slot

- Download the Win32DiskImager utility (it is also a zip file) - you can run this from a USB drive

- Extract the executable from the zip file and run the Win32DiskImager utility - you may need to run the utility as Administrator! Right-click on the file, and select *Run as Administrator*

- Select the image file you extracted above

- Select the drive letter of the SD card in the device box. Be careful to select the correct drive; if you get the wrong one you can destroy your data on the computer's hard disk! If you are using an SD Card slot in your computer (if you have one) and can't see the drive in the Win32DiskImager window, try using a cheap Adapter in a USB slot

- Click *Write* and wait for the write to complete

- Exit the imager and eject the SD card

### Mac OS

#### Graphical interface

- Connect the SD card reader with the SD card inside; note: must be formatted in FAT32

- From the Apple menu, choose About This Mac, then click on More info...; if you are using Mac OS X 10.8.x Mountain Lion then click on System report.

- Click on USB (or Card Reader if using an in-built SD card reader) then search for your SD card in the upper right section of the window; click it, then search for BSD name in the lower right section: must be something like diskn where n is a number (for example, disk4). Note this number

- Unmount the partition so that you will be allowed to overwrite the disk by opening Disk Utility and unmounting it (do not eject it, or you have to reconnect it). Note: On Mac OS X 10.8.x Mountain Lion, "Verify Disk" (before unmounting) will display the BSD name as "/dev/disk1s1" (or similar), allowing you to skip the previous two steps.

- From the Terminal run:
    - ```sudo dd if=path_of_your_image.img of=/dev/diskn bs=1m```
    - Remember to replace n with the number that you noted before!

#### Command line

- If you are comfortable with the command line, you can image a card without any additional software. Run:

    ```diskutil list```

- Identify the disk (not partition) of your SD card. e.g. ```disk4``` (not ```disk4s1```)
    
    ```diskutil unmountDisk /dev/<disk# from diskutil>```
    
    e.g. ```diskutil unmountDisk /dev/disk4```

    ```sudo dd bs=1m if=<your image file>.img of=/dev/<disk# from diskutil>```
    
    e.g. ```sudo dd bs=1m if=2012-12-16-wheezy-raspbian.img of=/dev/disk4```

    (This will take a few minutes)

**Alternatively:**

Note: Some users have reported issues with using Mac OS X to create SD cards.

These commands and actions need to be performed from an account that has administrator privileges.

- From the terminal run ```df -h```

- Connect the SD card reader with the SD card inside

- Run ```df -h``` again and look for the new device that wasn't listed last time. Record the device name of the filesystem's partition, for example, ```/dev/disk3s1```

- Unmount the partition so that you will be allowed to overwrite the disk:

    ```sudo diskutil unmount /dev/disk3s1```
    
    (or: open Disk Utility and unmount the partition of the SD card (do not eject it, or you have to reconnect it)

- Using the device name of the partition work out the raw device name for the entire disk, by omitting the final "s1" and replacing "disk" with "rdisk" (this is very important: you will lose all data on the hard drive on your computer if you get the wrong device name). Make sure the device name is the name of the whole SD card as described above, not just a partition of it (for example, rdisk3, not rdisk3s1. Similarly you might have another SD drive name/number like rdisk2 or rdisk4, etc. -- recheck by using the df -h command both before & after you insert your SD card reader into your Mac if you have any doubts!):

    For example, ```/dev/disk3s1``` => ```/dev/rdisk3```

- In the terminal write the image to the card with this command, using the raw disk device name from above (read carefully the above step, to be sure you use the correct rdisk# here!):

    ```sudo dd bs=1m if=~/Downloads/2012-10-28-wheezy-raspbian/2012-12-16-wheezy-raspbian.img of=/dev/rdisk3```

    If the above command report an error (```dd: bs: illegal numeric value```), please change ```bs=1M``` to ```bs=1m```

    (note that dd will not feedback any information until there is an error or it is finished, information will show and disk will re-mount when complete. However if you are curious as to the progresss - ctrl-T (SIGINFO, the status argument of your tty) will display some en-route statistics).

- After the dd command finishes, eject the card:

    ```sudo diskutil eject /dev/rdisk3```

    (or: open Disk Utility and eject the SD card)

### Linux

#### Using ImageWriter (graphical interface)

- Insert the SD card into your computer or connect the SD card reader with the SD card inside

- Install the ImageWriter tool from the Ubuntu Software Center

- Launch the ImageWriter tool (it needs your administrative password)

- Select the image file (example 2012-10-28-wheezy-raspbian.img) to be written to the SD card (note: because you started ImageWriter as administrator the starting point when selecting the image file is the administrator's home folder so you need to change to your own home folder to select the image file)

- Select the target device to write the image to (your device will be something like "/dev/mmcblk0" or "/dev/sdc")
Click the "Write to device" button

- Wait for the process to finish and then insert the SD card in the Raspberry Pi


#### Command line interface

Please note that the use of the ```dd``` tool can overwrite any partition of your machine. If you specify the wrong device in the instructions below you could delete your primary Linux partition. Please be careful.

- Run ```df -h``` to see what devices are currently mounted

- If your computer has a slot for SD cards, insert the card. If not, insert the card into an SD card reader, then connect the reader to your computer.

- Run ```df -h``` again. The device that wasn't there last time is your SD card. The left column gives the device name of your SD card. It will be listed as something like ```/dev/mmcblk0p1``` or ```/dev/sdd1```. The last part (```p1``` or ```1``` respectively) is the partition number, but you want to write to the whole SD card, not just one partition, so you need to remove that part from the name (getting for example ```/dev/mmcblk0``` or ```/dev/sdd```) as the device for the whole SD card. Note that the SD card can show up more than once in the output of df: in fact it will if you have previously written a Raspberry Pi image to this SD card, because the Raspberry Pi SD images have more than one partition.

- Now that you've noted what the device name is, you need to unmount it so that files can't be read or written to the SD card while you are copying over the SD image. So run the command below, replacing "/dev/sdd1" with whatever your SD card's device name is (including the partition number)
umount /dev/sdd1

- If your SD card shows up more than once in the output of df due to having multiple partitions on the SD card, you should unmount all of these partitions.
In the terminal write the image to the card with this command, making sure you replace the input file if= argument with the path to your ```.img``` file, and the ```/dev/sdd``` in the output file of= argument with the right device name (this is very important: you will lose all data on the hard drive on your computer if you get the wrong device name). Make sure the device name is the name of the whole SD card as described above, not just a partition of it (for example, ```sdd```, not ```sdds1``` or ```sddp1```, or ```mmcblk0``` not ```mmcblk0p1```)
    
    ```dd bs=4M if=~/2012-12-16-wheezy-raspbian.img of=/dev/sdd```
    
- Please note that block size set to ```4M``` will work most of the time, if not, please try ```1M```, although ```1M``` will take considerably longer.

- Note that if you are not logged in as root you will need to prefix this with sudo
The ```dd``` command does not give any information of its progress and so may appear to have frozen. It could take more than five minutes to finish writing to the card. If your card reader has an LED it may blink during the write process. To see the progress of the copy operation you can run pkill -USR1 -n -x dd in another terminal (prefixed with sudo if you are not logged in as root). The progress will be displayed (perhaps not immediately, due to buffering) in the original window, not the window with the pkill command.

    - Instead of ```dd``` you can use ```dcfldd```; it will give a progress report about how much has been written.

- You can check what's written to the SD card by dd-ing from the card back to your harddisk to another image, and then running diff (or md5sum) on those two images. There should be no difference.

- As root run the command sync or if a normal user run sudo sync (this will ensure the write cache is flushed and that it is safe to unmount your SD card)
Remove SD card from card reader