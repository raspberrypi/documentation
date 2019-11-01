# Copying an operating system image to an SD card using Mac OS

[balenaEtcher](README.md) is the best option for most users to write images to SD cards. 

**Note**: The use of the `dd` tool can overwrite any partition of your machine. If you specify the wrong device in the instructions, you could overwrite your primary Mac OS partition!

## Determine SD device

- Insert the SD card in the slot or connect the SD card reader with the SD card inside.


- `diskutil list`

    or

- From the Apple menu, choose 'System Report', then click on 'More info...'. 
- Click on 'USB' (or 'Card Reader' if you are using a built-in SD card reader), then search for your SD card in the upper right section of the window. Click on it, then search for the BSD name in the lower right section. It is in the form `diskN` (for example, `disk4`). Record this name.
- using Disk Utility, unmount the partition. Do not eject it. 

## Copy the image

- From Terminal, enter:
  ```
  sudo dd bs=1m if=path_of_your_image.img of=/dev/rdiskN conv=sync
  ```

   Replace `N` with the number that you noted before.
   
   This can take more than 15 minutes, depending on the image file size. 
   Check the progress by pressing Ctrl+T.
   
    If the command reports `dd: bs: illegal numeric value`, change the block size `bs=1m` to `bs=1M`.
    
    If the command reports `dd: /dev/rdisk2: Operation not permitted` you need to disable SIP before continuing.

    If the command reports the error `dd: /dev/rdisk3: Permission denied`, the partition table of the SD card is being protected against being overwritten by Mac OS. Erase the SD card's partition table using this command:
    
    ```
    sudo diskutil partitionDisk /dev/diskN 1 MBR "Free Space" "%noformat%" 100%
    ```
    
    That command will also set the permissions on the device to allow writing. Now issue the `dd` command again.

## After the `dd` command finishes, eject the card:

```
sudo diskutil eject /dev/rdiskN
```
