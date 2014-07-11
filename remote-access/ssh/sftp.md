# SFTP

The SSH File Transfer Protocol is a network protocol that provides file access, file transfer, and file management functionalities over SSH.

By using SFTP you can easily change, browse and edit files on your Raspberry Pi. SFTP is easier to setup than [FTP](../ftp.md) as Raspbian has SSH enabled by default.

## FileZilla

Download the latest FileZilla Client version for your operating system from [filezilla-project.org](https://filezilla-project.org/).

Launch FileZilla and go to `File > Site manager`.

Fill in the IP address, user name and password (by default the user name is `pi` and the password `raspberry`) of your Raspberry Pi in the dialog and choose `SFTP` as the protocol.

Click `Connect` and you will see the home folder of the user.

## Ubuntu using Nautilus

Open Nautilus on the client machine

Select `File > Connect to Server`

```
Type: SSH
Server: <The Pi's IP address>
Port: 22 (default)
User name: pi (default)
Password: raspberry (default)
```

See [IP address](../../troubleshooting/hardware/networking/ip-address.md).
