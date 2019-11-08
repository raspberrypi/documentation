# Using a proxy server

If you want your Raspberry Pi to access the internet via a proxy server (perhaps from a school or other workplace), you will need to configure your Pi to use the server before you can get online.

## What you will need

You will need:

+ The IP address or hostname and port of your proxy server
+ A username and password for your proxy (if required)

## Configuring your Pi

You will need to set up three environment variables (`http_proxy`, `https_proxy`, and `no_proxy`) so your Raspberry Pi knows how to access the proxy server.

+ Open a terminal window, and open the file `/etc/environment` using nano:

```
sudo nano /etc/environment
```

![open etc environment](images/proxy-open-environment.png)

+ Add the following to the `/etc/environment` file to create the `http_proxy` variable:

```
export http_proxy="http://proxyipaddress:proxyport"
```

+ Replace `proxyipaddress` and `proxyport` with the IP address and port of your proxy.

**Note**: if your proxy requires a username and password, add them using the following format:

```
export http_proxy="http://username:password@proxyipaddress:proxyport"
```

+ Enter the same information for the environment variable `https_proxy`:

```
export https_proxy="http://username:password@proxyipaddress:proxyport"
```
+ Create the `no_proxy` environment variable, which is a comma-separated list of addresses your Pi should not use the proxy for:

```
export no_proxy="localhost, 127.0.0.1"
```

Your `/etc/environment` file should now look like this:

```
export http_proxy="http://username:password@proxyipaddress:proxyport"
export https_proxy="http://username:password@proxyipaddress:proxyport"
export no_proxy="localhost, 127.0.0.1"
```

![environment variables](images/proxy-environment-variables.png)

+ Press <kbd>Ctrl + X</kbd> to save and exit.

## Update sudoers 

In order for operations that run as `sudo` (e.g. downloading and installing software) to use the new environment variables, you'll need to update `sudoers`.

+ Use the following command to open `sudoers`:

```
sudo visudo
```

+ Add the following line to the file so `sudo` will use the environment variables you just created:

```
Defaults	env_keep+="http_proxy https_proxy no_proxy"
```

![edit sudoers](images/proxy-edit-sudoers.png)

+ Press <kbd>Ctrl + X</kbd> to save and exit.

## Reboot

+ Reboot your Raspberry Pi for the changes to take effect.

You should now be able to access the internet via your proxy server.
