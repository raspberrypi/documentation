# Installing Operating System Images on Linux

On Linux systems you have the choice of the command line `dd` tool or using the graphical tool ImageWriter to write the image to your SD card.

## Using ImageWriter (graphical interface)

- Insert the SD card into your computer or connect the SD card reader with the SD card inside

- Install the ImageWriter tool from the Ubuntu Software Center

- Launch the ImageWriter tool (it needs your administrative password)

- Select the image file (e.g. `2014-01-07-wheezy-raspbian.img`) to be written to the SD card (note: because you started ImageWriter as administrator the starting point when selecting the image file is the administrator's home folder so you need to change to your own home folder to select the image file)

- Select the target device to write the image to (your device will be something like `/dev/mmcblk0` or `/dev/sdc`)

- Click the `Write to device` button

- Wait for the process to finish and remove the SD card

## Command line interface

Please note that the use of the `dd` tool can overwrite any partition of your machine. If you specify the wrong device in the instructions below you could delete your primary Linux partition. Please be careful.

- Run `df -h` to see what devices are currently mounted

- If your computer has a slot for SD cards, insert the card. If not, insert the card into an SD card reader, then connect the reader to your computer.

- Run `df -h` again. The device that wasn't there last time is your SD card. The left column gives the device name of your SD card. It will be listed as something like `/dev/mmcblk0p1` or `/dev/sdd1`. The last part (`p1` or `1` respectively) is the partition number, but you want to write to the whole SD card, not just one partition, so you need to remove that part from the name (getting for example `/dev/mmcblk0` or `/dev/sdd`) as the device for the whole SD card. Note that the SD card can show up more than once in the output of df: in fact it will if you have previously written a Raspberry Pi image to this SD card, because the Raspberry Pi SD images have more than one partition.

- Now that you've noted what the device name is, you need to unmount it so that files can't be read or written to the SD card while you are copying over the SD image.

- Run `umount /dev/sdd1` replacing `sdd1` with whatever your SD card's device name is (including the partition number)

- If your SD card shows up more than once in the output of `df` due to having multiple partitions on the SD card, you should unmount all of these partitions.

- In the Terminal, write the image to the card with this command, making sure you replace the input file `if=` argument with the path to your `.img` file, and the `/dev/sdd` in the output file `of=` argument with the right device name (this is very important: you will lose all data on the hard drive on your computer if you get the wrong device name). Make sure the device name is the name of the whole SD card as described above, not just a partition of it (for example, `sdd`, not `sdds1` or `sddp1`, or `mmcblk0` not `mmcblk0p1`)

    ```
    dd bs=4M if=2014-01-07-wheezy-raspbian.img of=/dev/sdd
    ```

- Please note that block size set to `4M` will work most of the time, if not, please try `1M`, although this will take considerably longer.

- Also note that if you are not logged in as root you will need to prefix this with sudo
    - The `dd` command does not give any information of its progress and so may appear to have frozen. It could take more than five minutes to finish writing to the card. If your card reader has an LED it may blink during the write process. To see the progress of the copy operation you can run `pkill -USR1 -n -x dd` in another terminal (prefixed with `sudo` if you are not logged in as root). The progress will be displayed (perhaps not immediately, due to buffering) in the original window, not the window with the `pkill` command.
    - Instead of `dd` you can use `dcfldd`; it will give a progress report about how much has been written.

- You can check what's written to the SD card by `dd`-ing from the card back to your harddisk to another image, and then running `diff` (or `md5sum`) on those two images. There should be no difference.

- ARun `sudo sync`. This will ensure the write cache is flushed and that it is safe to unmount your SD card.

- Remove SD card from card reader
