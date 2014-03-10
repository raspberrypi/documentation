# SSH using Linux

You can use SSH to connect to your Raspberry Pi from a Linux computer (or another Pi) from the Terminal, without installing additional software.

You'll need to know your Pi's IP address to connect to it. To find this, type `hostname -I` in the Terminal. Alternatively if you're running the Pi headless (without a screen), you can also look at the device list on your router or use a tool like `nmap`.

Copy and paste the following command into the Terminal window but replace `<IP>` with the IP address of the Raspberry Pi. Use `Ctrl + Shift + V` to paste in the Terminal.

```
ssh pi@<IP>
```

If you receive a `connection timed out` error it's likely that you've entered the wrong IP address for the Raspberry Pi.

When the connection works you'll see the security/authenticity warning below.

![](images/ssh/linux/ssh-ubuntu-login.png)

You will have to type *yes* to continue. You'll only see this warning the first time you connect to a Pi that it has never been seen by this computer before.

In the event your Pi has taken the IP address of a device to which your computer has connected before (even on another network), you may be given a warning and asked to clear the record from your list of known devices. Following this instruction and trying the `ssh` command again should be successful.

Next you'll be prompted for the password for the `pi` login, by default on Raspbian the password is `raspberry`. You should now have the Raspberry Pi prompt which will be identical to the one found on the Raspberry Pi itself.

If you have set up another user on the Pi, you can connect to it the same way, replacing the username with your own, e.g. `eben@192.168.1.5`

```
pi@raspberrypi ~ $
```

You are now connected to the Pi remotely and can execute commands.

For further documentation on the `ssh` command just enter `man ssh` into the Terminal.

## Passwordless login

It is possible to configure your Pi to allow your computer to access it without providing a password each time you try to connect. To do this you need to generate an SSH key:

### Check for existing SSH keys

First, check whether there are already keys on your computer (the one you're connecting from):

```
ls ~/.ssh
```

If you see files named `id_rsa.pub` or `id_dsa.pub` you have keys set up already, so you can skip the generating keys step (or delete these files with `rm id*` and make new keys).

### Generate new SSH keys

To generate new SSH keys enter the following command (Choose a sensible hostname such as `<YOURNANME>@<YOURDEVICE>` where we have used `eben@pi`):

```
ssh-keygen -t rsa -C eben@pi
```

You can also use a more descriptive comment using quotes if you have spaces, e.g. `ssh-keygen -t rsa -C "Raspberry Pi #123"`

Upon entering this command, you'll be asked where to save the key. We suggest you save it in the default location (`/home/pi/.ssh/id_rsa`) by just hitting `Enter`.

You'll also be asked to enter a passphrase. This is extra security which will make the key unusable without your passphrase, so if someone else copied your key, they could not impersonate you to gain access. If you choose to use a passphrase, type it here and press `Enter`, then type it again when prompted. Leave empty for no passphrase.

Now you should see the files `id_rsa` and `id_rsa.pub` in your `.ssh` directory in your home folder:

```
ls ~/.ssh
```

```
authorized_keys  id_rsa  id_rsa.pub  known_hosts
```

The `id_rsa` file is your private key. Keep this on your computer.

The `id_rsa.pub` file is your public key. This is what you put on machines you want to connect to. When the machine you try to connect to matches up your public and private key, it will allow you to connect.

Take a look at your public key to see what it looks like:

```
cat ~/.ssh/id_rsa.pub
```

It should be in the form:

```
ssh-rsa <REALLY LONG STRING OF RANDOM CHARACTERS> eben@pi
```

### Copy your public key to your Raspberry Pi

To copy your public key to your Raspberry Pi, use the following command to append the public key to your `authorized_keys` file on the Pi, sending it over SSH:

```
cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP-ADDRESS> 'cat >> .ssh/authorized_keys'
```

Note that this time you will have to authenticate with your password.

Now try `ssh <USER>@<IP-ADDRESS>` and you should connect without a password prompt.

If this did not work, delete your keys with `rm ~/.ssh/id*` and follow the instructions again.

You can also send files over SSH using the `scp` command (secure copy). See the [SCP guide](scp.md) for more information.
