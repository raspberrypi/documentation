# Passwordless SSH access

It is possible to configure your Pi to allow your computer to access it without providing a password each time you try to connect. To do this you need to generate an SSH key:

## Check for existing SSH keys

First, check whether there are already keys on the computer you are using to connect to the Raspberry Pi:

```bash
ls ~/.ssh
```

If you see files named `id_rsa.pub` or `id_dsa.pub` you have keys set up already, so you can skip the generating keys step (or delete these files with `rm id*` and make new keys).

## Generate new SSH keys

To generate new SSH keys enter the following command:

```bash
ssh-keygen
```

Upon entering this command, you'll be asked where to save the key. We suggest you save it in the default location (`/home/pi/.ssh/id_rsa`) by just hitting `Enter`.

You'll also be asked to enter a passphrase. This is extra security which will make the key unusable without your passphrase, so if someone else copied your key, they could not impersonate you to gain access. If you choose to use a passphrase, type it here and press `Enter`, then type it again when prompted. Leave the field empty for no passphrase.

Now look inside your `.ssh` directory:

```bash
ls ~/.ssh
```

and you should see the files `id_rsa` and `id_rsa.pub`:

```
authorized_keys  id_rsa  id_rsa.pub  known_hosts
```

The `id_rsa` file is your private key. Keep this on your computer.

The `id_rsa.pub` file is your public key. This is what you share with machines you want to connect to. When the machine you try to connect to matches up your public and private key, it will allow you to connect.

Take a look at your public key to see what it looks like:

```bash
cat ~/.ssh/id_rsa.pub
```

It should be in the form:

```bash
ssh-rsa <REALLY LONG STRING OF RANDOM CHARACTERS> user@host
```

<a name="copy-your-public-key-to-your-raspberry-pi"></a>
## Copy your public key to your Raspberry Pi

To copy your public key to your Raspberry Pi, use the following command, on the computer you will be connecting from, to append the public key to your `authorized_keys` file on the Pi, sending it over SSH:

```bash
ssh-copy-id <USERNAME>@<IP-ADDRESS>
```

**Note that this time you will have to authenticate with your password.**

Alternatively, if the `ssh-copy-id` is not available on your system, you can copy the file manually over SSH:

```bash
cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP-ADDRESS> 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
```

If you see the message `ssh: connect to host <IP-ADDRESS> port 22: Connection refused` and you know the `IP-ADDRESS` is correct, then you probably haven't enabled SSH on your Pi. Run `sudo raspi-config` in the Pi's terminal window, enable SSH, and then try to copy the files again.

Now try `ssh <USER>@<IP-ADDRESS>` and you should connect without a password prompt.

If you see a message "Agent admitted failure to sign using the key" then add your RSA or DSA identities to the authentication agent `ssh-agent` then execute the following command:

```bash
ssh-add
```

If this did not work, delete your keys with `rm ~/.ssh/id*` and follow the instructions again.

You can also send files over SSH using the `scp` command (secure copy). See the [SCP guide](scp.md) for more information.

## Let macOS store your passphrase so you don't have to enter it each time

If you're using macOS and after verifying that your new key allows you to connect, you can optionally choose to store the passphrase for your key in the macOS Keychain. This will make it so that you don't have to enter the passphrase each time you connect to your Pi.

Run the following command to store it in your keychain:

```bash
ssh-add -K ~/.ssh/id_rsa
```
