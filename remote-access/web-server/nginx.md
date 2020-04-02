# Setting up an NGINX web server on a Raspberry Pi

NGINX (pronounced *engine x*) is a popular lightweight web server application you can install on the Raspberry Pi to allow it to serve web pages.

Like Apache, NGINX can serve HTML files over HTTP, and with additional modules can serve dynamic web pages using scripting languages such as PHP.

## Refresh database of available packages

Ensure that the package manager has up-to-date information about which packages are available:  

```bash
sudo apt update
```

You only need to do this occasionally, but it's the most likely solution if subsequent steps fail with messages like:
```
  404  Not Found [IP: 93.93.128.193 80]
```

## Install NGINX

First install the `nginx` package by typing the following command in to the Terminal:

```bash
sudo apt install nginx
```

and start the server with:

```bash
sudo /etc/init.d/nginx start
```

## Test the web server

By default, NGINX puts a test HTML file in the web folder. This default web page is served when you browse to `http://localhost/` on the Pi itself, or `http://192.168.1.10` (whatever the Pi's IP address is) from another computer on the network. To find the Pi's IP address, type `hostname -I` at the command line (or read more about finding your [IP address](../ip-address.md)).

Browse to the default web page either on the Pi or from another computer on the network and you should see the following:

![NGINX welcome page](images/nginx-welcome.png)

### Changing the default web page

NGINX defaults its web page location to `/var/www/html` on Raspbian. Navigate to this folder and edit or replace index.nginx-debian.html as you like. You can confirm the default page location at `/etc/nginx/sites-available` on the line which starts with 'root', should you need to.


## Additional - Install PHP

```bash
sudo apt install php-fpm
```

### Enable PHP in NGINX

```bash
cd /etc/nginx
sudo nano sites-enabled/default
```

find the line

```
index index.html index.htm;
```

roughly around line 25 (Press `CTRL + C` in nano to see the current line number)

Add `index.php` after `index` to look like this:

```
index index.php index.html index.htm;
```

Scroll down until you find a section with the following content:

```
# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
#
# location ~ \.php$ {
```

Edit by removing the `#` characters on the following lines:

```
location ~ \.php$ {
	include snippets/fastcgi-php.conf;
	fastcgi_pass unix:/var/run/php5-fpm.sock;
}
```

It should look like this:

```
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        location ~ \.php$ {
                include snippets/fastcgi-php.conf;
        
		# With php-fpm (or other unix sockets):
		fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
		# With php-cgi (or other tcp sockets):
	#	fastcgi_pass 127.0.0.1:9000;
        }
```

Reload the configuration file

```bash
sudo /etc/init.d/nginx reload
```

### Test PHP

Rename `index.nginx-debian.html` to `index.php`:

```bash
cd /var/www/html/
sudo mv index.nginx-debian.html index.php
```

Open `index.php` with a text editor:

```bash
sudo nano index.php
```

Add some dynamic PHP content by replacing the current content:
```php
<?php echo phpinfo(); ?>
```

Save and refresh your browser. You should see a page with the PHP version, logo and current configuration settings.

What next! - I'll be adding a guide for using Lets Encrypt to add ssl to the Raspberry Pi nginx server.

In this tutorial, I’ll guide you through the process of installing let’s encrypt SSL certificates on your nginx powered website. By the end of the tutorial, we’ll have done the following:

Installed the let’s encrypt service
Generate a free let’s encrypt SSL certificate
Install free SSL certificate in nginx to secure your site
Secure site with SSL

Throughout this tutorial, I’ll be installing and configuring in Ubuntu 16.04, but the instructions will also work fine with Debian. I haven’t tested but there’s no reason why this tutorial won’t work to install SSL to your nginx site on Raspbian for a Raspberry Pi.

Let’s Encrypt is a free service which allows you to create short-life SSL certificates for your web application. It’s a great alternative to paying for SSL from the likes of GoDaddy or NameCheap.

Why secure your site with SSL?
SSL encrypts requests made between a web server and a visitors browser. This ensures requests and responses happen in a manner that can’t be intercepted. Furthermore, there’s a level of authentication which means that if an SSL certificate was intended for a different domain, the user is made aware and most modern browsers will block the request.

Google have a great article about HTTPS that I recommend anyone to read.

Step 1 – Install the Let’s Encrypt client
The installation is very straight forward. First, we’ll make sure we’re all up to date by installing updates and upgrades:

```sudo apt-get update && sudo apt-get upgrade```

Now we’ll install the Let’s Encrypt client:

```sudo apt-get install letsencrypt```

We’ve now installed the Let’s Encrypt client. This is what we’ll use to generate SSL certificates.

Step 2 – Generate a free SSL certificate
We’re ready to generate our first SSL certificate. I’m going to make two assumptions here, first that your site resides in /var/www/ and secondly that you want a certificate for your ‘www.’ subdomain. Run the following command to add an SSL certificate to your site, changing ‘example.com’ to suit your setup:

```sudo letsencrypt certonly --webroot -w /var/www/example.com -d example.com -d www.example.com```

This will create your certificate files in /etc/letsencrypt/live/example.com/.

Step 3 – Configure Nginx to use the SSL certificate
Finally, we need to make changes to our virtual host to tell it to use SSL. There’s going to be loads of assumptions coming up, so make sure you change your configuration to suit your needs. You may also need to force non-SSL traffic to your SSL site.

First, we generate some DH parameters. A great explanation of why we do this can be found at this stack exchange post. Switch directory:

```cd /etc/ssl/certs/```

Now generate the certificate:

```openssl dhparam -out dhparam.pem 4096```

I’m assuming that you are editing the built-in virtual host and that it has always worked. Below is a sample of how this might look after we’ve made our changes. I’ve highlighted the changed bits in red:

```sudo nano /etc/nginx/sites-available/default```

Then modify the file:

server { listen 443 ssl default_server; listen [::]:443 ssl default_server; ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem; ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # drop SSLv3 (POODLE vulnerabilit$ ssl_session_cache shared:SSL:10m; ssl_session_timeout 10m; ssl_dhparam /etc/ssl/certs/dhparam.pem; root /var/www/example.com; index index.html index.htm index.nginx-debian.html; server_name www.example.com example.com; location / { try_files $uri $uri/ =404; } location ~ .php$ { include snippets/fastcgi-php.conf; fastcgi_pass unix:/run/php/php7.0-fpm.sock; } location ~ /.ht { deny all; } }

Finally, we need to ensure the configuration isn’t broken. We do this by running the following command:

```sudo service nginx configtest```

If all’s well, go ahead and restart the service:

```sudo service nginx restart```

Go ahead, give your site a go. It should now be SSL secured – for free.

Conclusion

Not only have we added an SSL to our site, we’ve strengthened our configuring by adding DH parameters and setting our cyphers. Running our sites through some tests we can see everything’s in place:



Running some extended tests through SSLLabs we can see we get an A rating with this configuration.
