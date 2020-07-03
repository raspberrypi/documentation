# SSH using Windows 10

You can use SSH to connect to your Raspberry Pi from a Windows 10 computer that is using *October 2018 Update* or later without having to use third-party clients.

If you haven't already done so, go to Settings > Apps > Apps & features > Manage optional features > Add a feature, and choose to install *OpenSSH Client*.

You will need to know your Raspberry Pi's IP address to connect to it. To find this, type `hostname -I` from your Raspberry Pi terminal.

If you are running the Pi without a screen (headless), you can also look at the device list on your router or use a tool like `nmap`, which is described in detail in our [IP Address](../ip-address.md) document.

To connect to your Pi from a different computer, copy and paste the following command into the terminal window, but replace `<IP>` with the IP address of the Raspberry Pi. Use `Ctrl + Shift + V` to paste in the terminal.

```
ssh pi@<IP>
```

If you have set up another user on the Raspberry Pi, you can connect to it in the same way, replacing the default `pi` user with your own username, e.g. `ssh eben@192.168.1.5`.

If you receive a `connection timed out` error, it is likely that you have entered the wrong IP address for the Raspberry Pi.

When the connection works you will see a security/authenticity warning. Type `yes` to continue. You will only see this warning the first time you connect.

In the event that your Pi has taken the IP address of a device to which your computer has connected before (even if this was on another network), you may be given a warning and asked to clear the record from your list of known devices. Following this instruction and trying the `ssh` command again should be successful.

Next you will be prompted for the password for the user as which you are trying to connect: the default password for the `pi` user on Raspberry Pi OS is `raspberry`. For security reasons it is highly recommended to change the default password on the Raspberry Pi. You should now be able to see the Raspberry Pi prompt, which will be identical to the one found on the Raspberry Pi itself.

```
pi@raspberrypi ~ $
```

You are now connected to the Raspberry Pi remotely, and can execute commands.

To configure your Raspberry Pi to allow passwordless SSH access with a public/private key pair, see the [passwordless SSH](passwordless.md) guide.
