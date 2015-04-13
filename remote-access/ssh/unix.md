# SSH using Linux or Mac OS

You can use SSH to connect to your Raspberry Pi from a Linux computer or Mac (or another Pi) from the Terminal, without installing additional software.

You'll need to know your Pi's IP address to connect to it. To find this from your Pi's terminal type `hostname -I`.

Alternatively if you're running the Pi without a screen, aka headless, you can also look at the device list on your router or use a tool like `nmap`, which is described in detail in our [IP Address](../../troubleshooting/hardware/networking/ip-address.md) doc.

To connect to your Pi from a different computer, copy and paste the following command into the terminal window but replace `<IP>` with the IP address of the Raspberry Pi. Use `Ctrl + Shift + V` to paste in the terminal.

```
ssh pi@<IP>
```

If you receive a `connection timed out` error it's likely that you've entered the wrong IP address for the Raspberry Pi.

When the connection works you'll see a security/authenticity warning. Type `yes` to continue. You'll only see this warning the first time you connect.

In the event your Pi has taken the IP address of a device to which your computer has connected before (even on another network), you may be given a warning and asked to clear the record from your list of known devices. Following this instruction and trying the `ssh` command again should be successful.

Next you'll be prompted for the password for the `pi` login, by default on Raspbian the password is `raspberry`. You should now have the Raspberry Pi prompt which will be identical to the one found on the Raspberry Pi itself.

If you have set up another user on the Pi, you can connect to it the same way, replacing the username with your own, e.g. `eben@192.168.1.5`

```
pi@raspberrypi ~ $
```

You are now connected to the Pi remotely and can execute commands.

For further documentation on the `ssh` command just enter `man ssh` into the Terminal.

To configure your Pi to allow passwordless SSH access with a public/private key pair see the [passwordless SSH](passwordless.md) guide.
