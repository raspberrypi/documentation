# SFTP

The SSH File Transfer Protocol is a network protocol that provides file access, file transfer, and file management functionalities over SSH.

By using SFTP, you can easily change, browse, and edit files on your Raspberry Pi. SFTP is easier to set up than [FTP](../ftp.md) once Raspberry Pi OS has SSH enabled. For security reasons, since the November 2016 release of Raspberry Pi OS, the SSH server has been disabled by default. To enable it, please follow [these instructions](./README.md).)

## WinSCP on Windows

We recommend using the [WinSCP SFTP client](https://winscp.net/eng/index.php). Follow the instructions on the WinSCP website to install the client, then follow the [WinSCP Quick Start instructions](https://winscp.net/eng/docs/getting_started).

## FileZilla on Linux

Install FileZilla on your Linux system using the standard package manager for your distribution (e.g. `sudo apt install filezilla`).

Launch FileZilla and go to **File > Site manager**.

Fill in the [IP address](../ip-address.md), username and password (by default the username is `pi` and the password `raspberry`) of your Raspberry Pi in the dialog and choose **SFTP** as the protocol.

Click `Connect` and you will see the home folder of the user.

## Ubuntu using Nautilus

Open Nautilus on the client machine.

Select **File > Connect to Server**.

```
Type: SSH
Server: <The Pi's IP address>
Port: 22 (default)
User name: pi (default)
Password: raspberry (default)
```
## Chrome OS file manager (tested on Acer Chromebook)

Open the Chromebook's file manager app.

Scroll to the bottom of the file tree in the left panel.

Click **Add new services**

```
Select and click
SFTP file system
```

In the dialogue box that opens, enter:

```
The IP address or
The hostname (default is `raspberrypi`)
Enter port 22 (Not the one shown next to the IP address on your pi)
Add user `pi` and the password (default is `raspberry`)
```
You may encounter another dialogue box for security; if you do, click **Allow** or **Accept**. 
