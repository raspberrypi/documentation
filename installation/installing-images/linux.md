# Installing operating system images on Linux

[Raspberry Pi Imager](README.md) is typically the easiest option for most users to write images to SD cards, so it is a good place to start. If you're looking for more advanced options on Linux, you can use the standard command line tools below.

**Note**: use of the `dd` tool can overwrite any partition of your machine. If you specify the wrong device in the instructions below, you could delete your primary Linux partition. Please be careful.

### Discovering the SD card mountpoint and unmounting it
- Run `lsblk -p` to see which devices are currently connected to your machine.

- If your computer has a slot for SD cards, insert the card. If not, insert the card into an SD card reader, then connect the reader to your computer.

- Run `lsblk -p` again. The new device that has appeared is your SD card (you can also usually tell from the listed device size). The naming of the device will follow the format described in the next paragraph.

- The left column of the results from the `lsblk -p` command gives the device name of your SD card and the names of any partitions on it (usually only one, but there may be several if the card was previously used). It will be listed as something like `/dev/mmcblk0` or `/dev/sdX` (with partition names `/dev/mmcblk0p1` or `/dev/sdX1` respectively), where `X` is a lower-case letter indicating the device (eg. `/dev/sdb1`). The right column shows where the partitions have been mounted (if they haven't been, it will be blank).

- If any partitions on the SD card have been mounted, unmount them all with `umount`, for example `umount /dev/sdX1` (replace `sdX1` with your SD card's device name, and change the number for any other partitions).

### Copying the image to the SD card

- In a terminal window, write the image to the card with the command below, making sure you replace the input file `if=` argument with the path to your `.img` file, and the `/dev/sdX` in the output file `of=` argument with the correct device name. **This is very important, as you will lose all the data on the hard drive if you provide the wrong device name.** Make sure the device name is the name of the whole SD card as described above, not just a partition. For example: `sdd`, not `sdds1` or `sddp1`; `mmcblk0`, not `mmcblk0p1`.

    ```bash
    dd bs=4M if=2020-08-20-raspios-buster-armhf.img of=/dev/sdX conv=fsync
    ```

- Please note that block size set to `4M` will work most of the time. If not,  try `1M`, although this will take considerably longer.

- Also note that if you are not logged in as root you will need to prefix this with `sudo`.

### Copying a zipped image to the SD card

In Linux it is possible to combine the unzip and SD copying process into one command, which avoids any issues that might occur when the unzipped image is larger than 4GB. This can happen on certain filesystems that do not support files larger than 4GB (e.g. FAT), although it should be noted that most Linux installations do not use FAT and therefore do not have this limitation.

The following command unzips the zip file (replace 2020-08-20-raspios-buster-armhf.zip with the appropriate zip filename), and pipes the output directly to the dd command. This in turn copies it to the SD card, as described in the previous section.
```
unzip -p 2020-08-20-raspios-buster-armhf.zip | sudo dd of=/dev/sdX bs=4M conv=fsync
```

### Checking the image copy progress

- By default, the `dd` command does not give any information about its progress, so it may appear to have frozen. It can take more than five minutes to finish writing to the card. If your card reader has an LED, it may blink during the write process.

- To see the progress of the copy operation, you can run the dd command with the status option.
   ```
    dd bs=4M if=2020-08-20-raspios-buster-armhf.img of=/dev/sdX status=progress conv=fsync
   ```
- If you are using an older version of `dd`, the status option may not be available. You may be able to use the `dcfldd` command instead, which will give a progress report showing how much has been written. Another method is to send a USR1 signal to `dd`, which will let it print status information. Find out the PID of `dd` by using `pgrep -l dd` or `ps a | grep dd`. Then use `kill -USR1 PID` to send the USR1 signal to `dd`.

### Optional: checking whether the image was correctly written to the SD card

- After `dd` has finished copying, you can check what has been written to the SD card by `dd`-ing from the card back to another image on your hard disk, truncating the new image to the same size as the original, and then running `diff` (or `md5sum`) on those two images.

- If the SD card is much larger than the image, you don't want to read back the whole SD card, since it will be mostly empty. So you need to check the number of blocks that were written to the card by the `dd` command. At the end of its run, `dd` will have displayed the number of blocks written as follow:
```
xxx+0 records in
yyy+0 records out
yyyyyyyyyy bytes (yyy kB, yyy KiB) copied, 0.00144744 s, 283 MB/s
```
We need the number `xxx`, which is the block count. We can ignore the `yyy` numbers.

- Copy the SD card content to an image on your hard drive using `dd` again:
    ```bash
    dd bs=4M if=/dev/sdX of=from-sd-card.img count=xxx
    ```
`if` is the input file (i.e. the SD card device), `of` is the output file to which the SD card content is to be copied (called `from-sd-card.img` in this example), and `xxx` is the number of blocks written by the original `dd` operation.

- In case the SD card image is still larger than the original image, truncate the new image to the size of the original image using the following command (replace the input file `reference` argument with the original image name):
    ```bash
    truncate --reference 2020-08-20-raspios-buster-armhf.img from-sd-card.img
    ```
- Compare the two images: `diff` should report that the files are identical.
    ```bash
    diff -s from-sd-card.img 2020-08-20-raspios-buster-armhf.img
    ```
- Run `sync`. This will ensure that the write cache is flushed and that it is safe to unmount your SD card.

- Remove the SD card from the card reader.
