# FTP

FTP (File Transfer Protocol) can be used to transfer files between a Raspberry Pi and another computer. Although with default program `sftp-server` of Raspbian the users with sufficient privilege can transfer files or directories, access to the filesystem of the limited users is also required oftenly. Follow the steps below to set up an FTP server:

## Install Pure-FTPd

Firstly install `Pure-FTPd` using the following command line in Terminal:

```bash
sudo apt-get install pure-ftpd
```

## Basic Configurations

We need to creat a new user group named `ftpgroup` and a new user named `ftpuser` for FTP users, and make sure this "user" has NO log in privilge and NO home directory:

```bash
groupadd ftpgroup;
useradd ftpuser -g ftpgroup -s /sbin/nologin –d /dev/null
```

### FTP Home Directory, Virtual User, and User Group

For instance, make a new directory named `FTP` for the first user:

```bash
sudo mkdir /home/pi/FTP
```

Make sure the directory is accessable for `ftpuser`:

```bash
sudo chown -R ftpuser:ftpgroup /home/pi/FTP
```

Create a virtual user named `upload`, mapping the virtual user to `ftpuser` and `ftpgroup`, setting home directory `/home/pi/FTP`, and record password of the user in database:

```bash
sudo pure-pw useradd upload -u ftpuser -g ftpgroup -d /home/pi/FTP -m
```

A password of that virtual user will be required after this command line is entered. And next, set up a virtual user database by typing:

```bash
sudo pure-pw mkdb
```

Last but not least, define an authentication method by making a link of file `/etc/pure-ftpd/conf/PureDB`, the number `60` is only for demonstration, make it as small as necessary:

```bash
ln -s /etc/pure-ftpd/conf/PureDB /etc/pure-ftpd/auth/60puredb
```

Restart the program:

```bash
sudo service pure-ftpd restart
```

Test it with an FTP client, like FileZilla.

## More Detailed Configurations:

The configuration of Pure-FTPd is simple and intuitive. The administrator only needs to define the necessary settings by making files with option names, like `ChrootEveryone`, and typing `yes`, then storing in the directory `/etc/pure-ftpd/conf`, if all FTP users are to be locked in their FTP home directory (`/home/pi/FTP`). Here are some recommended settings:

```bash
sudo nano /etc/pure-ftpd/conf/ChrootEveryone
```

Type `yes`, and press ``Ctrl+X``, ``Y``, and ``Enter``.

Likewise,

make a file named `NoAnonymous` and type `yes`;

make a file named `AnonymousCantUpload` and type `yes`;

make a file named `AnonymousCanCreateDirs` and type `no`;

make a file named `DisplayDotFiles` and type`no`;

make a file named `DontResolve` and type `yes`;

make a file named `ProhibitDotFilesRead` and type `yes`;

make a file named `ProhibitDotFilesWrite` and type `yes`;

make a file named `FSCharset` and type`UTF-8`;

...

Restart `pure-ftpd` again and apply the above settings.

```bash
sudo service pure-ftpd restart
```

For more information of Pure-FTPd and documentation, please get on official website of [Pure-FTPd](http://www.pureftpd.org/project/pure-ftpd).
