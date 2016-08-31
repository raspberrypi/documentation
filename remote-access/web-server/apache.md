# Setting up an Apache Web Server on a Raspberry Pi

Apache is a popular web server application you can install on the Raspberry Pi to allow it to serve web pages.

On its own, Apache can serve HTML files over HTTP, and with additional modules can serve dynamic web pages using scripting languages such as PHP.

## Install Apache

First install the `apache2` package by typing the following command in to the Terminal:

```bash
sudo apt-get install apache2 -y
```

## Test the web server

By default, Apache puts a test HTML file in the web folder. This default web page is served when you browse to `http://localhost/` on the Pi itself, or `http://192.168.1.10` (whatever the Pi's IP address is) from another computer on the network. To find the Pi's IP address, type `hostname -I` at the command line (or read more about finding your [IP address](../ip-address.md)).

Browse to the default web page either on the Pi or from another computer on the network and you should see the following:

![Apache success message](images/apache-it-works.png)

This means you have Apache working!

### Changing the default web page

This default web page is just a HTML file on the filesystem. It is located at `/var/www/html/index.html`.

**Note: The directory was `/var/www` in Raspbian Wheezy but is now `/var/www/html` in Raspbian Jessie**

Navigate to this directory in the Terminal and have a look at what's inside:

```
cd /var/www/html
ls -al
```

This will show you:

```bash
total 12
drwxr-xr-x  2 root root 4096 Jan  8 01:29 .
drwxr-xr-x 12 root root 4096 Jan  8 01:28 ..
-rw-r--r--  1 root root  177 Jan  8 01:29 index.html
```

This shows that there is one file in `/var/www/html/` called `index.html`. The `.` refers to the directory itself `/var/www/html` and the `..` refers to the parent directory `/www/`.

### What the columns mean

1. The permissions of the file or directory
2. The number of files in the directory (or `1` if it's a file).
3. The user which owns the file or directory
4. The group which owns the file or directory
5. The file size
6. The last modification date & time

As you can see, by default the `html` directory and `index.html` file are both owned by the `root` user. In order to edit the file, you must gain `root` permissions. Change the owner to your own user with `sudo chown pi: index.html` before editing.

Try editing this file and refreshing the browser to see the web page change.

### Your own website

If you know HTML you can put your own HTML files and other assets in this directory and serve them as a website on your local network.

## Additional - install PHP

To allow your Apache server to process PHP files, you'll need to install PHP5 and the PHP5 module for Apache. Type the following command to install these:

```bash
sudo apt-get install php5 libapache2-mod-php5 -y
```

Now remove the `index.html` file:

```bash
sudo rm index.html
```

and create the file `index.php`:

```bash
sudo leafpad index.php
```

*Note: Leafpad is a graphical editor. Alternatively, use `nano` if you're restricted to the command line*

Put some PHP content in it:

```php
<?php echo "hello world"; ?>
```

Now save and refresh your browser. You should see "hello world". This is not dynamic but still served by PHP. Try something dynamic:

```php
<?php echo date('Y-m-d H:i:s'); ?>
```

or show your PHP info:

```php
<?php phpinfo(); ?>
```

### Further - WordPress

Now you have Apache and PHP installed you can progress to setting up a WordPress site on your Pi. Continue to [WordPress usage](../../usage/wordpress/README.md).
