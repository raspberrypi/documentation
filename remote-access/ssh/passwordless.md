# Passwordless SSH access

It is possible to configure your Raspberry Pi to allow access from another computer without needing to provide a password each time you connect. To do this, you need to use an SSH key instead of a password. To generate an SSH key:

## Check for existing SSH keys

First, check whether there are already keys on the computer you are using to connect to the Raspberry Pi:

```bash
ls ~/.ssh
```

If you see files named `id_rsa.pub` or `id_dsa.pub` then you have keys set up already, so you can skip the 'Generate new SSH keys' step below.

## Generate new SSH keys

To generate new SSH keys enter the following command:

```bash
ssh-keygen
```

Upon entering this command, you will be asked where to save the key. We suggest saving it in the default location (`~/.ssh/id_rsa`) by pressing `Enter`.

You will also be asked to enter a passphrase, which is optional. The passphrase is used to encrypt the private SSH key, so that if someone else copied the key, they could not impersonate you to gain access. If you choose to use a passphrase, type it here and press `Enter`, then type it again when prompted. Leave the field empty for no passphrase.

Now look inside your `.ssh` directory:

```bash
ls ~/.ssh
```

and you should see the files `id_rsa` and `id_rsa.pub`:

```
authorized_keys  id_rsa  id_rsa.pub  known_hosts
```

The `id_rsa` file is your private key. Keep this on your computer.

The `id_rsa.pub` file is your public key. This is what you share with machines that you connect to: in this case your Raspberry Pi. When the machine you try to connect to matches up your public and private key, it will allow you to connect.

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


Using the computer which you will be connecting from, append the public key to your `authorized_keys` file on the Raspberry Pi by sending it over SSH:

```bash
ssh-copy-id <USERNAME>@<IP-ADDRESS>
```

**Note that for this step you will need to authenticate with your password.**

Alternatively, if `ssh-copy-id` is not available on your system, you can copy the file manually over SSH:

```bash
cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP-ADDRESS> 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
```

If you see the message `ssh: connect to host <IP-ADDRESS> port 22: Connection refused` and you know the `IP-ADDRESS` is correct, then you may not have enabled SSH on your Raspberry Pi. Run `sudo raspi-config` in the Pi's terminal window, enable SSH, then try to copy the files again.

Now try `ssh <USER>@<IP-ADDRESS>` and you should connect without a password prompt.

If you see a message "Agent admitted failure to sign using the key" then add your RSA or DSA identities to the authentication agent `ssh-agent` then execute the following command:

```bash
ssh-add
```

If this does not work, you can get assistance on the [Raspberry Pi forums](https://www.raspberrypi.org/forums/).

**Note:** you can also send files over SSH using the `scp` command (secure copy). See the [SCP guide](scp.md) for more information.

## Store the passphrase in the macOS keychain

If you are using macOS, and after verifying that your new key allows you to connect, you have the option of storing the passphrase for your key in the macOS keychain. This allows you to connect to your Raspberry Pi without entering the passphrase.

Run the following command to store it in your keychain:

```bash
ssh-add -K ~/.ssh/id_rsa
```
