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

Alternatively, you can use the `pv` command to see a progress meter as the dumpfile is processed by MySQL. This is not installed by default, so install with `sudo apt-get install pv`. This command is useful for large files:

```bash
pv recipes.sql | mysql recipes
```

## SD card image

It may be sensible for you to keep a copy of the entire SD card image, so you can restore the card if you lose it or it becomes corrupt. You can do this using the same method you'd use to write an image to a new card, but in reverse.

In Linux or on a Mac, for example:

```bash
sudo dd bs=4M if=/dev/sdb of=raspbian.img
```

This will create an image file on your computer which you can use to write to another SD card, and keep exactly the same contents and settings. To restore or clone to another card, use `dd` in reverse:

```bash
sudo dd bs=4M if=raspbian.img of=/dev/sdb
```

These files can be very large, and compress well. To compress, you can pipe the output of `dd` to `gzip` to get a compressed file that is significantly smaller than the original size:

```bash
sudo dd bs=4M if=/dev/sdb | gzip > rasbian.img.gz
```

To restore, pipe the output of `gunzip` to `dd`:

```bash
gunzip --stdout rasbian.img.gz | sudo dd bs=4M of=/dev/sdb
```

See more about [installing SD card images](../../installation/installing-images/README.md).

## Automation

You could write a Bash script to perform each of these processes automatically, and even have it performed periodically using [cron](../usage/cron.md).
