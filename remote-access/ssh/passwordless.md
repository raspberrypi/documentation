# Passwordless SSH access

It is possible to configure your Pi to allow your computer to access it without providing a password each time you try to connect. To do this you need to generate an SSH key:

## Check for existing SSH keys

First, check whether there are already keys on your computer (the one you're connecting from):

```
ls ~/.ssh
```

If you see files named `id_rsa.pub` or `id_dsa.pub` you have keys set up already, so you can skip the generating keys step (or delete these files with `rm id*` and make new keys).

## Generate new SSH keys

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

The `id_rsa` file is your private key, keep this on your computer and keep it safe. If you loose your private key then you will have to create a new one and repeat this process. If someone gets access to your private key, then they can do everything you can do (e.g., access your computer, unencrypt your stuff).

The `id_rsa.pub` file is your public key. This is what you put on machines you want to connect to. When the machine you try to connect to matches up your public and private key, it will allow you to connect.

Take a look at your public key to see what it looks like:

```
cat ~/.ssh/id_rsa.pub
```

It should be in the form:

```
ssh-rsa <REALLY LONG STRING OF RANDOM CHARACTERS> eben@pi
```

A slightly more useful command is to view your key's finger print:

```
ssh-keygen -l -f ~/.ssh/id_rsa.pub
```

You should see something like this:

```
2048 bc:f9:28:63:ff:4c:5d:4c:e1:59:7c:ed:6b:fe:d8:52  eben@pi- (RSA)
```

The problem is people cannot remember all of those numbers to determine if something is wrong with the server they are logging into or they key they are using. So another useful method is:

```
ssh-keygen -lv -f ~/.ssh/id_rsa.pub
```

This will generate an ASCII picture of your fingerprint, which is much easier for a human to interpret.

```
2048 bc:f9:28:63:ff:4c:5d:4c:e1:59:7c:ed:6b:fe:d8:52  eben@pi- (RSA)
+--[ RSA 2048]----+
|              ..o|
|             . ++|
|              +..|
|       .     o  .|
|        S     o .|
|         o . . oE|
|        o . . o. |
|      +  =    .+ |
|     . +o.+   ..+|
+-----------------+
```

## Copy your public key to your Raspberry Pi

To copy your public key to your Raspberry Pi, use the following command:

```
ssh-copy-id <USERNAME>@<IP-ADDRESS>
```

Note that this time you will have to authenticate with your password. `ssh-copy-id` will automatically update the ~/.ssh/authorized_keys file and ensure the correct permissions are applied to the file.

Now try `ssh <USER>@<IP-ADDRESS>` and you should connect without a password prompt.

If you see a message "Agent admitted failure to sign using the key." then add your RSA or DSA identities to the authentication agent, ssh-agent 
the execute the following command:  
```
ssh-add
```

If this did not work, delete your keys with `rm ~/.ssh/id*` and follow the instructions again.

You can also send files over SSH using the `scp` command (secure copy). See the [SCP guide](scp.md) for more information.

### Macs

Note that `ssh-copy-id` is not natively on OSX. You need to install [`brew`](http://brew.sh) and then execute:

```
brew update
brew install ssh-copy-id
```

Additionally, brew has a ton of other useful command line tools available for our mac. 

## Disable Password Logins Over SSH

Passwords have become inherently weak. Any password a person can think of, a computer can guess. Now that we have setup a strong Public Key Infrastructure (PKI), it is a liability to leave password logins enabled.

**Note:** You can always login via passwords directly in Raspberry Pi by using a keyboard. This only effect remote logins via SSH.

Edit using `sudo nano /etc/sshd_config` to disable password logins by changing the following parameters to `no`:

```
PasswordAuthentication no
ChallengeResponseAuthentication no
```
