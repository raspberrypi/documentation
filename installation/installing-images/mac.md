# Copying an operating system image to an SD card using Mac OS

[Raspberry Pi Imager](README.md) is the recommended option for most users to write images to SD cards.

## Determine SD device

- Insert the SD card in the slot or connect the SD card reader with the SD card inside.

### Command Line

- `diskutil list`

    Example (the SD card is /dev/disk2 - your disk and partition list may vary):

    ```bash
    ❯ diskutil list
    /dev/disk0 (internal):
        #:                       TYPE NAME                    SIZE       IDENTIFIER
        0:                       GUID_partition_scheme        500.3 GB   disk0
        1:                       EFI EFI                      314.6 MB   disk0s1
        2:                       Apple_APFS Container disk1   500.0 GB   disk0s2

    /dev/disk1 (synthesized):
        #:                       TYPE NAME                    SIZE       IDENTIFIER
        0:                       APFS Container Scheme -      +500.0 GB   disk1
                                 Physical Store disk0s2
        1:                       APFS Volume Macintosh HD     89.6 GB    disk1s1
        2:                       APFS Volume Preboot          47.3 MB    disk1s2
        3:                       APFS Volume Recovery         510.4 MB   disk1s3
        4:                       APFS Volume VM               3.6 GB     disk1s4

    /dev/disk2 (external, physical):
        #:                       TYPE NAME                    SIZE       IDENTIFIER
        0:                       FDisk_partition_scheme       *15.9 GB    disk2
        1:                       Windows_FAT_32 boot          268.4 MB   disk2s1
        2:                       Linux                        15.7 GB    disk2s2
    ```

### Graphical / Disk Utility

- From the Apple menu, choose 'System Report', then click on 'More info...'.
- Click on 'USB' (or 'Card Reader' if you are using a built-in SD card reader), then search for your SD card in the upper right section of the window. Click on it, then search for the BSD name in the lower right section.
It is in the form `diskN` (for example, `disk4`).
Record this name.
- using Disk Utility, unmount the partition.
Do not eject it.

## Copy the image

### Command Line

**Note**: The use of the `dd` tool can overwrite any partition of your machine.
If you specify the wrong device in the instructions, you could overwrite your primary Mac OS partition!

- The disk must be unmounted before copying the image

    ```bash
    diskutil unmountDisk /dev/diskN
    ```

- Copy the image

  ```bash
  sudo dd bs=1m if=path_of_your_image.img of=/dev/rdiskN; sync
  ```

   Replace `N` with the number that you noted before. Note the ```rdisk``` ('raw disk')
   instead of ```disk```, this speeds up the copying.   

   This can take more than 15 minutes, depending on the image file size.
   Check the progress by pressing Ctrl+T.
   
    If the command reports `dd: /dev/rdiskN: Resource busy`, you need to unmount the volume first `sudo diskutil unmountDisk /dev/diskN`.

    If the command reports `dd: bs: illegal numeric value`, change the block size `bs=1m` to `bs=1M`.

    If the command reports `dd: /dev/rdiskN: Operation not permitted`, go to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Files and Folders` -> `Give Removable Volumes access to Terminal`.

    If the command reports `dd: /dev/rdiskN: Permission denied`, the partition table of the SD card is being protected against being overwritten by Mac OS. Erase the SD card's partition table using this command:
    
    ```
    sudo diskutil partitionDisk /dev/diskN 1 MBR "Free Space" "%noformat%" 100%
    ```

    That command will also set the permissions on the device to allow writing.
    Now issue the `dd` command again.

## Eject

After the `dd` command finishes, eject the card:

```bash
sudo diskutil eject /dev/rdiskN
```
