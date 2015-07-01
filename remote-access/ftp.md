# FTP

FTP (File Transfer Protocol) can be used to transfer files between a Raspberry Pi and another computer. Although with default program `sftp-server` of Raspbian the users with sufficient privilege can transfer files or directories, access to the filesystem of the limited users is also required oftenly. Follow the the steps below to set up an FTP server:

## Install Pure-FTPd

Firstly install `Pure-FTPd` using terminal, and type the following line:

```bash
sudo apt-get install pure-ftpd
```

## Configuration

The configuration of Pure-FTPd is simple and intuitive, and the administrator only need to define the necessary settings. However, before we start setting-up, we need to creat a new user group named `ftpgroup` and a new user named `ftpuser` without shell log in priviledg for FTP users:

```bash
groupadd ftpgroup;
useradd ftpuser -s /sbin/nologin
```

### Virtual User and User Group


