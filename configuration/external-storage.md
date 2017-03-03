# External Storage configuration
You can connect your external hard disk drive (HDD) to any of the two USB2.0 ports on the Raspberry Pi and mount it to access the data stored on your HDD. 

**NOTE:** The following instructions require that your Raspberry Pi is running Raspbian.

If your HDD has an exFAT partition, first install the exFAT driver.

## Installing the exFAT driver
Run the following command in the command line to install the exFAT driver using the Aptitude Package Manager. 
```
sudo apt-get install exfat-fuse
```

## Mounting a HDD 

1. Plug-in the external HDD to a USB port on the Raspberry Pi. 
2. List the disk partitions on the device. Run the following command: 
    ```
    sudo blkid
    ```

3. Note the location of the disk partition. For example, `/dev/sda1`.
4. Create a target folder to be the mount point of the HDD. Run the following command: 
    ```
    sudo mkdir /mnt/PIHDD
    ```

5. Mount the HDD from the location of the partition to the mount point. Run the following command:  
    ```
    sudo mount /dev/sda1 /mnt/PIHDD
    ```

6. Verify that the HDD is mounted successfully by listing the content. Run the following command: 
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

## Unmounting a HDD
Before you unmount your HDD, ensure that there are no programs accessing the HDD.

1. Run the following command to get the list of programs using the mount point: 
    ```
    lsof /mnt/PIHDD
    ```

2. End all programs using the mount point. Run the following command: 
    ```
    sudo kill 13827
    ```
   
   where, `13827` is the PID.  
    
 **NOTE:** Ensure that you save your changes before running the `kill` command.
3. Unmount the HDD. Run the following command:  
    ```
    sudo umount /mnt/PIHDD
    ```

4. Unplug the HDD and delete the mount point folder . Run the following command: 
    ```
    sudo rmdir /mnt/PIHDD
    ```
