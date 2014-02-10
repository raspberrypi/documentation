# WordPress

Here we'll show you how to set up an instance of a WordPress site running on your Raspberry Pi using the Apache Web Server

## Set up the web server

First of all, follow the steps to [set up an Apache web server](../remote-access/web-servers/apache.md), then return here to continue with the WordPress installation

## Install PHP and MySQL

You need to install some additional tools for WordPress to run on the web server.

### PHP

PHP is a preprocessor, it's code that runs when the server receives a request for a web page. It runs, works out what needs to be shown on the page, then sends that page to the browser. Unlike static HTML, PHP can show different content under different circumstances. Other languages are capable of this, but since WordPress is written in PHP, that's what we need this time. PHP is a very popular language on the web: large projects like Facebook and Wikipedia are written in PHP.

Install the PHP and Apache

```
sudo apt-get install php5 libapache2-mod-php5 -y
```

### MySQL

MySQL (pronounced *My Sequel* or *My S-Q-L*) is a popular database engine. Like PHP, its overwhelming presence on web servers enhanced its popularity, which is why projects like WordPress use it (and why those projects are so popular).

Install the MySQL Server and PHP-MySQL packages by entering the following command in to the terminal:

```
sudo apt-get install mysql-server php5-mysql -y
```

## Download WordPress

You can download WordPress from [wordpress.org](http://wordpress.org/) using the ```wget``` command. Helpfully, a copy of the latest version of WordPress is always available at [wordpress.com/latest.tar.gz](http://wordpress.com/latest.tar.gz) and [wordpress.com/latest.zip](http://wordpress.com/latest.zip) so you can grab the latest version without having to look it up on the website.

Navigate to ```/var/www/``` and download WordPress to this location:

```
cd /var/www
wget http://wordpress.com/latest.tar.gz
```

Now extract the tarball, move the contents of the folder it extracted (```wordpress```) to the current directory and remove the (now empty) folder:

```
tar xzf latest.tar.gz
mv wordpress/* .
rm -rf wordpress
```

Running the ```ls``` or (```tree -L 1```) command here will show you the contents of a WordPress project:

```
.
├── index.php
├── wp-activate.php
├── wp-admin
├── wp-blog-header.php
├── wp-comments-post.php
├── wp-config-sample.php
├── wp-content
├── wp-cron.php
├── wp-includes
├── wp-links-opml.php
├── wp-load.php
├── wp-login.php
├── wp-mail.php
├── wp-settings.php
├── wp-signup.php
├── wp-trackback.php
└── xmlrpc.php
```

