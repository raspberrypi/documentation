# External Storage configuration
You can connect your external hard disk drive (HDD) to any of the USB ports on the Raspberry Pi, and mount the file system to access the data stored on your HDD. 

By default, Raspberry Pi automatically mounts some of the popular file systems such as FAT, NTFS, and HFS+ at `/media/pi/<HARD-DRIVE-LABEL>` location.

To set up your HDD so that it always mounts to a specific location of your choice, you must manually mount your HDD.

## Mounting an HDD 
You can mount your HDD at a specific folder location. It is conventional to do this within the /mnt folder, for example /mnt/PIHDD. Note that the folder must be empty. If the folder is not empty, the system will not mount the HDD.

1. Plug in the external HDD to a USB port on the Raspberry Pi. 
2. List all the disk partitions on the Pi using the following command:

    ```
    sudo lsblk -o UUID,NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,MODEL
    ```
   The Raspberry Pi uses mount points `/` and `/boot`. Your HDD will show up in this list, along with any other connected storage.
3. Use the SIZE, LABEL, and MODEL columns to identify the name of the disk partition that points to your HDD. For example, `sda1`. 
4. The FSTYPE column contains the filesystem type. If your HDD uses an exFAT file system, install the exFAT driver:

    ```
    sudo apt-get update
    sudo apt-get install exfat-fuse
    ```
5. If your HDD uses an NTFS file system, you will have read-only access to the HDD. If you want to write to the HDD, you can install the ntfs-3g driver:

    ```
    sudo apt-get update
    sudo apt-get install ntfs-3g
    ```
6. Run the following command to get the location of the disk partition:

    ```
    sudo blkid
    ```
    For example, `/dev/sda1`.
7. Create a target folder to be the mount point of the HDD. 
   The mount point name used in this case is `PIHDD`. You can specify a name of your choice:

    ```
    sudo mkdir /mnt/PIHDD
    ```
8. Mount the HDD at the mount point you created:

    ```
    sudo mount /dev/sda1 /mnt/PIHDD
    ```
9. Verify that the HDD is mounted successfully by listing the contents:

    ```
    ls /mnt/PIHDD
    ```

## Setting up automatic mounting
You can modify the `fstab` file to define the location where the HDD will be automatically mounted when the Raspberry Pi starts up. In the `fstab` file, the disk partition is identified by the universally unique identifier (UUID).

1. Get the UUID of the disk partition:

    ```
    sudo blkid
    ```
2. Find the disk partition from the list and note the UUID. For example, `5C24-1453`.
3. Edit the fstab file using a command line editor such as nano:

    ```
    sudo nano /etc/fstab
    ```
4. Add the following line in the `fstab` file:

    ```
    UUID=5C24-1453 /mnt/PIHDD FSTYPE defaults,auto,umask=000,users,rw,nofail 0 0
    ```
   Replace FSTYPE with the type of your file system, which you found in step 2 of 'Mounting an HDD' above.

Now that you have set an entry in `fstab`, you can start up your Raspberry Pi with or without the HDD attached. Before you disconnect the HDD you must either shut down the Pi, or manually unmount the HDD using the steps in 'Unmounting an HDD' below.

**Note:** if you do not have the HDD attached when the Pi starts, the Pi will take an extra 90 seconds to start up. You can shorten this by adding `,x-systemd.device-timeout=30` immediately after `nofail` in step 4. This will change the timeout to 30 seconds - so the system will only wait 30 seconds before giving up trying to mount the disk.

For more information on the Linux commands, refer to the specific manual pages using the `man` command. For example, `man fstab`.

## Unmounting an HDD
When the Raspberry Pi shuts down, the system takes care of unmounting the HDD so that it is safe to remove it. If you want to manually unmount an HDD, you can use the following command:

    ```
    sudo umount /mnt/PIHDD
    ```
    
If you receive an error that the 'target is busy', this means that the HDD was not unmounted. If no error was displayed, you can now safely unplug the HDD.

### Dealing with 'target is busy'
    
The 'target is busy' message means there are files on the HDD that are in use by a program. To close the files, use the following procedure.

1. Close any program which has open files on the HDD.

2. If you have a terminal open, make sure that the current working directory is not in the folder where the HDD is mounted, or a sub-folder of it. The current working directory is usually displayed next to the command prompt in the terminal window. The following is an example of the prompt displayed when the current working directory is /mnt/PIHDD:

    ```
    pi@raspberry:/mnt/PIHDD $
    ```
3. If you are still unable to unmount the HDD, you can use the `lsof` tool to check which program has files open on the HDD. You need to first install `lsof` using `apt-get`:

    ```
    sudo apt-get update
    sudo apt-get install lsof
    ```
   To use lsof:
   
    ```
    lsof /mnt/PIHDD
    ```
