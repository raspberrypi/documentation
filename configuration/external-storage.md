# External Storage configuration
You can connect your external hard disk drive (HDD) to any of the USB ports on the Raspberry Pi, and mount the file system to access the data stored on your HDD. 

By default, Raspberry Pi automatically mounts some of the popular file systems such as FAT, NTFS, and HFS+ at `/media/pi/<HARD-DRIVE-LABEL>` location. 

To set up your HDD so that it always mounts to a specific location of your choice, you must manually mount your HDD.

If your HDD has an exFAT partition, install the exFAT driver.

## Installing the exFAT driver
Run the following commands in the command line to update the Aptitude repository, then install the exFAT driver using the Aptitude Package Manager. 
```
sudo apt-get update
sudo apt-get install exfat-fuse
```

## Mounting an HDD 
You can mount your HDD at specific empty folder locations.

1. Plug in the external HDD to a USB port on the Raspberry Pi. 
2. List the disk partitions on the device. Run the following command: 

    ```
    sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL
    ```
   The Raspberry Pi uses mount points `/` and `/boot`.
3. Use the SIZE, LABEL, and MODEL columns to identify the name of the disk partition that points to your HDD. For example, `sda1`. 
4. Run the following command to get the location of the disk partition.

    ```
    sudo blkid
    ```
    For example, `/dev/sda1`.
5. Create a target folder to be the mount point of the HDD. 
   The mount point name used in this case is `PIHDD`. You can specify a name of your choice. 
   Run the following command: 

    ```
    sudo mkdir /mnt/PIHDD
    ```
6. Mount the HDD from the location of the partition to the mount point you created. Run the following command:  

    ```
    sudo mount /dev/sda1 /mnt/PIHDD
    ```
7. Verify that the HDD is mounted successfully by listing the content. Run the following command: 

    ```
    ls /mnt/PIHDD
    ```

## Setting up automatic mounting
You can modify the `fstab` file to define the location where the HDD will be automatically mounted when the Raspberry Pi starts up. In the `fstab` file, the disk partition is identified by the universally unique identifier (UUID). 

1. Get the UUID of the disk partition. Run the following command:  

    ```
    sudo blkid
    ```
2. Find the disk partition from the list and note the UUID. For example, `5C24-1453`.
3. Edit the fstab file using a command line editor such as nano. Run the following command: 

    ```
    sudo nano /etc/fstab
    ```
4. Add the following line in the `fstab` file. 

    ```
    UUID=5C24-1453 /mnt/PIHDD exfat defaults,auto,umask=000,users,rw 0 0
    ```

For more information on the Linux commands, refer to the specific manual pages using the `man` command. For example, `man fstab`.

## Unmounting an HDD
Before you unmount your HDD, ensure that there are no programs accessing the HDD. You can do this using the `lsof` command. 

1. Run the following commands to install `lsof`.

    ```
    sudo apt-get update
    sudo apt-get install -y lsof
    ```
2. Get the list of programs using the mount point: 

    ```
    lsof /mnt/PIHDD
    ```
   where `PIHDD` is the mount point name.
3. Manually close all the programs that are using the mount point.  
4. Unmount the HDD. Run the following command:  

    ```
    sudo umount /mnt/PIHDD
    ```
5. Unplug the HDD and delete the mount point folder . Run the following command: 

    ```
    sudo rmdir /mnt/PIHDD
    ```
