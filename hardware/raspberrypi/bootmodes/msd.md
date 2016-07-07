# How to boot from a USB Mass Storage Device on a Raspberry Pi 3
When the Raspberry Pi 3 was announced it was also mentioned that it had the capability to boot from USB Mass Storage Devices or via the network. This document describes the current method to configure a standard Rasbian image in such a way that can use these new boot modes
**WARNING: This is very experimental and only available to selected tests users**

## preparing the Rasberry Pi3
Before we can boot the Raspberry Pi3 from a USB Mass Storage Device (MSD Boot) we need to enable this option on the Rasberry Pi3. This is done using a special setting in the config.txt.

1. Download a standard Rasbian image and use the standard methodes to write it a normal SD Card.
https://www.raspberrypi.org/documentation/installation/installing-images/README.md

2. After writing the image reinsert the new image so that the "boot"  FAT patition of the SD card is mounted in your operating system.

3. replace the bootcode.bin and start.elf files with the new version of these two files

4. Open config.txt with an text editor and add the following line to the bottom the config.txt file

		program_usb_boot_mode=1

5. Put the adjusted SD Card into the Raspberry Pi3 and let it boot once from this SD Card.

6. Verify if the Raspberry Pi3 has the new USB boot modes activated by running the following command:

        vcgencmd otp_dump

7. This should produce a list of settings. Make sure that lines 17 and 18 are showing the following:

          17:3020000a
          18:3020000a

8. Now you know that this Raspberry Pi3 is USB boot enabled.

## Writing the USB MSD

Now that your Rasberry Pi3 is USB Boot enabled you can start creating a USB Stick that you can use for your first boot. For this we ofcourse use the Raspberry Pi itself

1. Insert your empty USB MSD into a free USB slot of the Raspberry Pi3 **warning: all information on this USB MSD will be lost**

2. Download the latest Rasbian image from the Raspberry Pi website and unzip into a directory

3. Determine the correct device of the USB MSD and write the Rasbian image to it using the linux instructions on the website

4. After writing the image you should remove the USB MSD and then reinsert it again so that Rasbian will mount the two paritions on it

5. Check where the two partitions are mounted on the Raspberry Pi using the following command

             mount

6. It should show somewhere a line that looks like this

       /dev/sda1 on /media/pi/boot
       /dev/sda2 on /media/pi/2f84--something-long--231c

7. Go to the boot partition mount point and also replace the bootcode.bin and start.elf files on the USB MSD device
  
8. add the following line to the config.txt file in the boot partition

        dtoverlay=mmc

9. Adjust the cmdline.txt to remove the "init=/usr/lib/raspi-config/init_resize.sh" part and change the "root=/dev/mmcblk0p2" to "root=/dev/sda2" it should then look like this

          dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/sda2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet 

10. Go the root directory mount point on the Raspberry Pi3 and edit the /etc/fstab file to point to /dev/sda1 and /dev/sda2 for boot and root

11. Shutdown your Raspberry Pi3 and remove the SD Card (leave the USB MSD in the RaspBerry Pi3)

12. Power cycle the Raspberry Pi3 (unplug/plug USB Power supply) and watch the Raspberry Pi3 boot from the newly created USB MSD.

13. Be proud of your self :-)
