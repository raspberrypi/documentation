# Backups

It is highly recommended that you keep regular backups of any important files. Backups are often not limited to user files; they could include configuration files, databases, installed software, settings, and even an entire snapshot of a system.

Here, we'll guide you through some backup techniques for your Raspberry Pi system.

## Home folder

A sensible way to keep your home folder backed up is to use the `tar` command to make a snapshot archive of the folder, and keep a copy of it on your home PC or in cloud storage. To do this, enter the following commands:

```bash
cd /home/
sudo tar czf pi_home.tar.gz pi
```

This creates a tar archive called `pi_home.tar.gz` in `/home/`. You should copy this file to a USB stick or transfer it to another machine on your network.

## SD card copier (recommended)

The SD Card Copier application, which can be found on the `Accessories` menu of the Raspberry Pi Desktop, will copy Raspberry Pi OS from one card to another. To use it, you will need a USB SD card writer.

To back up your existing Raspberry Pi OS installation, put a blank SD card in your USB card writer and plug it into your Pi, and then launch SD Card Copier. In the ‘Copy From Device’ box, select the internal SD Card. This could have a number of different names, and may have something like `(/dev/mmcblk0)` in its entry, but will usually be the first item in the list. Then select the USB card writer in the ‘Copy To Device’ box (where it will probably be the only device listed). Press ‘Start’. The copy, depending on the size of the SD card, can take ten or fifteen minutes, and when complete you should have a clone of your current installation on the new SD card. You can test it by putting the newly-copied card into the Pi’s SD card slot and booting it; it should boot and look exactly the same as your original installation, with all your data and applications intact.

You can run directly from the backup, but if you want to recover your original card from your backup, simply reverse the process – boot your Pi from the backup card, put the card to which you want to restore into the SD card writer, and repeat the process above.

The program does not restrict you to only copying to a card the same size as the source; you can copy to a larger card if you are running out of space on your existing one, or even to a smaller card (as long as it has enough space to store all your files – the program will warn you if there isn’t enough space). It has been designed to work with Raspberry Pi OS and NOOBS images; it may work with other OSes or custom card formats, but this is not guaranteed.

The only restriction is that you cannot write to the internal SD card reader, as that would overwrite the OS you are actually running, which could break the installation completely.

Note, everything on the destination card will be overwritten, so ensure you do not have any critical data on it before starting the copy.

## SD card image

It may be sensible for you to keep a copy of the entire SD card image, so you can restore the card if you lose it or it becomes corrupt. You can do this using the same method you'd use to write an image to a new card, but in reverse.

In Linux:

```bash
sudo dd bs=4M if=/dev/sdb of=PiOS.img
```

This will create an image file on your computer which you can use to write to another SD card, and keep exactly the same contents and settings. To restore or clone to another card, use `dd` in reverse:

```bash
sudo dd bs=4M if=PiOS.img of=/dev/sdb
```

These files can be very large, and compress well. To compress, you can pipe the output of `dd` to `gzip` to get a compressed file that is significantly smaller than the original size:

```bash
sudo dd bs=4M if=/dev/sdb | gzip > PiOS.img.gz
```

To restore, pipe the output of `gunzip` to `dd`:

```bash
gunzip --stdout PiOS.img.gz | sudo dd bs=4M of=/dev/sdb
```

If you are using a Mac, the commands used are almost exactly the same, but `4M` in the above examples should be replaced with `4m`, with a lower case letter.

See more about [installing SD card images](../../installation/installing-images/README.md).

## MySQL

If you have MySQL databases running on your Raspberry Pi, it would be wise to keep them backed up too. To back up a single database, use the `mysqldump` command:

```bash
mysqldump recipes > recipes.sql
```

This command will back up the `recipes` database to the file `recipes.sql`. Note that, in this case, no username and password have been supplied to the `mysqldump` command. If you don't have your MySQL credentials in a `.my.cnf` configuration file in your home folder, then supply the username and password with flags:

```bash
mysqldump -uroot -ppass recipes > recipes.sql
```

To restore a MySQL database from a dumpfile, pipe the dumpfile into the `mysql` command. Provide credentials, if necessary, and the database name. Note that the database must exist, so create it first:

```bash
mysql -Bse "create database recipes"
cat recipes.sql | mysql recipes
```

Alternatively, you can use the `pv` command to see a progress meter as the dumpfile is processed by MySQL. This is not installed by default, so install with `sudo apt install pv`. This command is useful for large files:

```bash
pv recipes.sql | mysql recipes
```


## Automation

You could write a [Bash script](../usage/scripting.md) to perform each of these processes automatically, and even have it performed periodically using [cron](../usage/cron.md).
