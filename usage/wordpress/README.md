# WordPress

Here we'll show you how to set up an instance of a WordPress site to run on your Raspberry Pi using the Apache Web Server.

![Wordpress logo](images/wordpress-logo.png)

## Set up the web server

First of all, follow the steps to [set up an Apache web server](../../remote-access/web-server/apache.md), then return here to continue with the WordPress installation

## Install PHP and MySQL

You need to install some additional tools for WordPress to run on the web server. Type these commands in the terminal after logging in; if you booted to the desktop, open up LXTerminal and run them from there.

### PHP

PHP is a preprocessor; it's code that runs when the server receives a request for a web page. It runs, works out what needs to be shown on the page, then sends that page to the browser. Unlike static HTML, PHP can show different content under different circumstances. Other languages are capable of this, but since WordPress is written in PHP, that's what we need to use this time. PHP is a very popular language on the web; large projects like Facebook and Wikipedia are written in PHP.

![PHP logo](images/php-logo.png)

Install the PHP and Apache packages with the following command:

```bash
sudo apt-get install php5 libapache2-mod-php5 -y
```

### MySQL

MySQL (pronounced *My Sequel* or *My S-Q-L*) is a popular database engine. Like PHP, its overwhelming presence on web servers enhanced its popularity. This is why projects like WordPress use it, and why those projects are so popular.

![MySQL logo](images/mysql-logo.png)

Install the MySQL Server and PHP-MySQL packages by entering the following command into the terminal:

```bash
sudo apt-get install mysql-server php5-mysql -y
```

When installing MySQL you will be asked for a root password. You'll need to remember this to allow your website to access the database.

## Download WordPress

You can download WordPress from [wordpress.org](http://wordpress.org/) using the `wget` command. Helpfully, a copy of the latest version of WordPress is always available at [wordpress.org/latest.tar.gz](https://wordpress.org/latest.tar.gz) and [wordpress.org/latest.zip](https://wordpress.org/latest.zip), so you can grab the latest version without having to look it up on the website. At the time of writing, this is version 3.8.1.

Navigate to `/var/www/`, and download WordPress to this location. You'll need to empty the folder first (be sure to check you're not deleting files you need before running `rm`); change the ownership of this folder to the `pi` user too.

```bash
cd /var/www
sudo chown pi: .
rm *
wget http://wordpress.org/latest.tar.gz
```

Now extract the tarball, move the contents of the folder it extracted (`wordpress`) to the current directory and remove the (now empty) folder and the tarball to tidy up:

```bash
tar xzf latest.tar.gz
mv wordpress/* .
rm -rf wordpress latest.tar.gz
```

Running the `ls` or (`tree -L 1`) command here will show you the contents of a WordPress project:

```bash
.
├── index.php
├── license.txt
├── readme.html
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

This is the source of a default WordPress installation. The files you edit to customise your installation belong in the `wp-content` folder.

## Your WordPress database

To get your WordPress site set up, you need a database. Run the `mysql` command in the terminal, and provide your login credentials (e.g. username `root`, password `password`):

```bash
mysql -uroot -ppassword
```

Here I have provided my password (the word `password`) on the command line; there is no space between `-p` and your password.

Alternatively you can simply supply an empty `-p` flag and wait to be asked for a password:

```bash
mysql -uroot -p
```

Now you will be prompted to enter the root user password you created earlier.

Once you're connected to MySQL, you can create the database your WordPress installation will use:

```
mysql> create database wordpress;
```

Note the semicolon ending the statement. On success you should see the following message:

```
Query OK, 1 row affected (0.00 sec)
```

Exit out of the MySQL prompt with `Ctrl + D`.

## WordPress configuration

You need to find out your Pi's IP address to access it in the browser, so in a terminal type the command `hostname -I`.

Navigate to `http://YOUR-IP-ADDRESS` e.g. `http://192.168.1.5` in the web browser on your Pi.

You should see a WordPress Error page; this is good! Click the big button marked `Create a Configuration File` followed by the `Let's go!` button on the next page.

Now fill out the basic site information as follows:

```
Database Name:      wordpress
User Name:          root
Password:           <YOUR PASSWORD>
Database Host:      localhost
Table Prefix:       wp_
```

Upon successful database connection, you will be given the contents of your `wp-config.php` file:

![wp-config file](images/wp-config.png)

Copy this text, return to the terminal on the Pi and edit the file with `nano wp-config.php`. Paste the text into this file, and save and exit with `Ctrl + X`, then `Y` for yes and `Enter`.

Now hit the `Run the install` button.

### Welcome screen

Now you're getting close.

![Wordpress welcome screen](images/wp-info.png)

Fill out the information: give your site a title, create a username and password, put in your email address and untick the search engines box. Hit the `Install WordPress` button, then log in using the account you just created.

Now you're logged in and have your site set up, you can see the website by visiting your IP address in the browser on the Pi or another computer on the network. To log in again (or on another computer), go to `http://YOUR-IP-ADDRESS/wp-admin`.

It's recommended that you change your permalink settings to make your URLs more friendly. To do this, log in to WordPress and go to the dashboard. Go to `Settings` then `Permalinks`. Select the `Post name` option and click `Save Changes`. After saving, you will be prompted to update your `.htaccess` file. You probably don't have one yet, so add one in `/var/www/` by typing `nano .htaccess`; note this is a hidden file, so it starts with a dot. Then paste in the contents provided:

```
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
```

Save the file and return to the website homepage. Click on the post title or the sample page link and you'll probably see a `Not Found` error page. This is because the `rewrite` module has not been enabled in Apache. To do this, enter `sudo a2enmod rewrite`.

You'll also need to tell the virtual host serving the site to allow requests to be overwritten. Do this by editing the virtual host file (with root permissions): `sudo nano /etc/apache2/sites-available/default`; also, change the `AllowOverride` setting on line 11 (inside the `<Directory /var/www/>` block) from `None` to `All`. Save the file and then restart Apache with `sudo service apache2 restart`. Once it's restarted, refresh the page and it should load successfully. Now posts have URLs like `/hello-world/` instead of `/?p=123`, and pages have URLs like `/sample-page/` instead of `/?page_id=2`.

## Customisation

WordPress is very customisable. By clicking your site name in the WordPress banner along the top of the page (when logged in), you'll be taken to the Dashboard. From here you can change the theme, add pages and posts, edit the menu, add plugins and lots more. This is just a taster for getting something interesting set up on the Raspberry Pi's web server.
