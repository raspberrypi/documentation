# SSH using Linux or Mac OS

You can use SSH to connect to your Raspberry Pi from a Linux computer, a Mac, or another Raspberry Pi, without installing additional software.

You will need to know your Raspberry Pi's IP address to connect to it. To find this, type `hostname -I` from your Raspberry Pi terminal.

If you are running the Pi without a screen (headless), you can also look at the device list on your router or use a tool like `nmap`, which is described in detail in our [IP Address](../ip-address.md) document.

To connect to your Pi from a different computer, copy and paste the following command into the terminal window but replace `<IP>` with the IP address of the Raspberry Pi. Use `Ctrl + Shift + V` to paste in the terminal.

```
ssh pi@<IP>
```

If you receive a `connection timed out` error it is likely that you have entered the wrong IP address for the Raspberry Pi.

When the connection works you will see a security/authenticity warning. Type `yes` to continue. You will only see this warning the first time you connect.

In the event your Pi has taken the IP address of a device to which your computer has connected before (even if this was on another network), you may be given a warning and asked to clear the record from your list of known devices. Following this instruction and trying the `ssh` command again should be successful.

Next you will be prompted for the password for the `pi` login: the default password on Raspberry Pi OS is `raspberry`. For security reasons it is highly recommended to change the default password on the Raspberry Pi. You should now be able to see the Raspberry Pi prompt, which will be identical to the one found on the Raspberry Pi itself.

If you have set up another user on the Raspberry Pi, you can connect to it in the same way, replacing the username with your own, e.g. `eben@192.168.1.5`

```
pi@raspberrypi ~ $
```

You are now connected to the Pi remotely, and can execute commands.

## X-forwarding

You can also forward your X session over SSH, to allow the use of graphical applications, by using the `-Y` flag:

```bash
ssh -Y pi@192.168.1.5
```
Note that [X11 is no longer present on Macs with OSX](https://support.apple.com/en-gb/HT201341), so you will have to [download](https://www.xquartz.org/) and install it.

Now you are on the command line as before, but you have the ability to open up graphical windows. For example, typing:

```bash
geany &
```

will open up the Geany editor in a graphical window.

Typing:

```bash
scratch &
```

will open up Scratch.

For further documentation on the `ssh` command just enter `man ssh` into the Terminal.

To configure your Pi to allow passwordless SSH access with a public/private key pair, see the [passwordless SSH](passwordless.md) guide.
