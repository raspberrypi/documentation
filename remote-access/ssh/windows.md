# SSH using Windows

On Windows you will need to download an SSH client. The most commonly used one is called PuTTY and can be downloaded from [greenend.org.uk](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)

Look for `putty.exe` under the heading `For Windows on Intel x86`.

##1. Add your Raspberry Pi as a host
PuTTY doesn't have an installer package, it's just a standalone `.exe` file. When you run it you'll see the configuration screen below:

![PuTTY configuration](images/ssh-win-config.png)

Type the IP address of the Pi into the `Host Name` field and click the `Open` button. If nothing happens when you click the `Open` button, and you eventually see a message saying `Network error: Connection timed out`, it's likely that you've entered the wrong IP address for the Pi.

If you don't know the IP address, just type `hostname -I` in the Raspberry Pi command line. There are more ways to find your IP address [here](../ip-address.md).

##2. Connect
When the connection works you'll see the security warning shown below; you can safely ignore it and click the Yes button. You'll only see this warning the first time when PuTTY connects to a Pi that it has never seen before.

![PuTTY warning](images/ssh-win-warning.png)

You'll now have the usual login prompt. Log in with the same username and password you would use on the Pi itself. The default login for Raspbian is `pi` with the password `raspberry`.

You should now have the Raspberry Pi prompt which will be identical to the one found on the Raspberry Pi itself.

```
pi@raspberrypi ~ $
```

![PuTTY window](images/ssh-win-window.png)

You can type `exit` to close the PuTTY window.

##3. Modification, troubleshooting, and more
The next time you use PuTTY, look for the `Saved Sessions` section on the bottom half of the configuration screen. If you use this, we recommend switching to the `Connection` page in the left hand tree and setting the `Seconds between keepalives` value to `30`. Then switch back to the `Session` page in the tree before you click `Save`. Using this setting allows you to leave a PuTTY window open for long periods of time with no activity without the Pi timing out and disconnecting you.

A connection might be unsuccessful due to various reasons. It is most likely your device or Raspberry Pi are [not connected properly](../../configuration/wireless/wireless-cli.md), [SSH is disabled](../../configuration/raspi-config.md), you might have made a typo, or the IP address or credentials might have changed. In the latter cases, you need to update the host. For instructions on how to update a host and for further PuTTY documentation please see the [PuTTY docs](http://www.chiark.greenend.org.uk/~sgtatham/putty/docs.html).


