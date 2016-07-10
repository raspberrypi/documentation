#SSH USING iOS

To use SSH on your mobile device you need to download a client. There are several different good quality clients available, such as [Serverauditor](http://www.serverauditor.com), [Prompt 2](https://panic.com/prompt/), and  [Cathode](http://www.secretgeometry.com/apps/cathode/). 

For the sake of this tutorial we'll use Serverauditor, because it's a popular cross platform SSH client. But the principle is applicable to other clients as well. 

##1. Add your Raspberry Pi as a host.
Download Serverauditor from [iTunes](https://itunes.apple.com/en/app/serverauditor-ssh-shell-console/id549039908?mt=8), if you haven’t installed it yet. Click to open the app.

A prompt asking you to allow notifications will pop up. You should click ‘Allow’ (recommended). Now follow the instructions on the screen: `Start by adding a new host`. Tap `New Host` and a new window will pop up.

![Serverauditor ‘New Host’ configuration](images/ssh-ios-config.png)

Enter an `alias`; this could be ‘Raspberry Pi’, for example. Then enter the IP address under `hostname`. Complete the `username` and `password` fields and hit ‘save’ in the top right corner. 

If you don't know the IP address just type `hostname -I` in the command line on the Raspberry Pi. See [here](../ip-address.md) for more methods of finding your IP address. The default login for Raspbian is `pi` with the password `raspberry`.


##2. Connect

After you’ve saved the new host, you’ll be sent back to the ‘Hosts’ screen. There you’ll find the new entry. Make sure your mobile device has WiFi turned on and is connected to the same network as your Raspberry Pi.

Tap the new entry once; when the connection works you’ll see a [security warning](http://www.lysium.de/blog/index.php?/archives/186-How-to-get-ssh-server-fingerprint-information.html). Don’t worry, everything is fine, and you can click ‘Continue’. You’ll only see this warning the first time Serverauditor connects to a Pi that it hasn’t seen before.

![Serverauditor ‘Security warning’](images/ssh-ios-warning.png)

You should now have the Raspberry Pi prompt which will be identical to the one found on the Raspberry Pi itself.

```
pi@raspberrypi ~ $
```

You can type `exit` to close the terminal window.

![Serverauditor Terminal](images/ssh-ios-window.png)

If a red exclamation mark appears, this indicates that something went wrong. Tap the exclamation mark for the error description. ‘Connection establishment time out’ means you have probably entered an incorrect IP address. Otherwise, WiFi on your mobile device might be turned off, the Raspberry Pi might be turned off,  or it might be connected to a different network from your mobile device.

##3. Modify an entry, troubleshooting, and more
A connection might be unsuccessful for various reasons. It is likely that your device or Raspberry Pi is [not connected properly](../../configuration/wireless/wireless-cli.md), [SSH is disabled](../../configuration/raspi-config.md), you might have made a typo in your code, or the IP address or credentials have changed. In the latter cases, you need to update the host.

To do so, go to the ‘Hosts’ screen, swipe left on the host you need to edit, and new functions will appear. Tap edit. A new screen titled ‘Edit Host’ will pop up.
