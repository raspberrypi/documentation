# Securing your Raspberry Pi

Security of your Raspberry Pi is important. Gaps in security leave your Raspberry Pi open to hackers who can then use it without your permission.

What level of security you need depends on how you wish to use your Raspberry Pi. For example, if you are simply using your Raspberry Pi on your home network, behind a router with a firewall, then it already quite secure by default.

However, if you wish to expose your Raspberry Pi directly to the internet, either with a direct connection (unlikely) or by letting certain protocols through your router firewall (e.g. SSH), then you need to make some basic security changes.

Even if you are hidden behind a 

## Change your default password

The default username and password is used for every single Raspberry Pi running Raspbian. So, if you can get access to a Raspberry Pi, and these setting shave not been changed, you have `root` access to that Raspberry Pi.

So the first thing to do is change the password. This can be done via the raspi-config application, or from the command line.
```
sudo raspi-config
```
Select option 2, and follow the instructions to change the password.

In fact, all raspi-config does is start up the command line `passwd` application, which you can do from the command line. Simply type in your new password and confirm it.
```
sudo passwd
```
## Changing your username

Of course, you can be more secure by also changing your username. All Raspberry Pi's come with the default username `pi`, so by changing/removing that you are imediately more secure.

To add a new user with the same permissions as the `pi` user
```
sudo useradd -m fred -G sudo
```
This adds a new user called `fred`, creates a home folder, and adds the user to the `sudo` group. You now need to set a password for the new user
```
sudo passwd fred
```

Logout and log back with the new account details. Check your permissions are in place (i.e. you can sudo) by trying the following.
```
sudo visudo
```
`visudo` can only be run by an account with sudo privileges, so if it works OK, then the new account is in the `sudo` group.

Once the account is confirmed OK, delete the `pi` user
```
sudo deluser pi
```
This will leave the `home/pi` folder. If necessary you can use the following to remove the home folder for the `pi` user at the same time - note the data in this folder will be permanently deleted so make sure any require data is moved elsewhere.
```
sudo deluser -remove-home pi
```


## Improving SSH Security

SSH is a common way of accessing a Raspberry Pi remotely. By default, logging in with SSH requires a username/password pair, but a more secure method is to use key based authorisation.

Key pairs are two, cryptographically secure, keys. On is private, one is public, and they can be used to authenticate a client to an SSH server (in this case the Raspberry Pi). 

The client generates two keys, cryptographically linked to each other. The private key should never be released, but the public key can be freely shared. The SSH server takes a copy of the public key, and when a link is requested, uses this key to send the client a challenge message, which the client will encrypt using the private key. If the server can then decrypt this message using the public key back to the original challenge message then the identity of the client is confirmed. 

Generating a key pair in Linux is done using the `ssh-keygen` command on the ***client***, and by default the keys are stored in the `.ssh` folder in the users home directly. The private key will be called id_rsa and the associated public key will be called id_rsa.pub. The key will be 2048 bits long and breaking the encryption on a key of that length would take an extremely long time, so is very secure. You can make longer keys if the situation demands it. Note that you should only do the generation process once, if repeated it will overwrite any previous generated keys. ANything relying on those old keys will need to be updated to the new keys. 

You will be prompted for a passphrase during key generation, this is an extra level of security. For the moment leave this blank.

The public key now needs to be moved on to the server. This can be done by email, or cut and paste, or file copying. Once on the server it needs to be added to the SSH systems authorised keys. It should be emphasised that the `id_rsa` file is the private key and SHOULD NOT LEAVE THE CLIENT, whilst the public key file is `id_rsa.pub`.

Add the new public key to the authorisation file as follows:
```
cat id_rsa.pub >> ~/.ssh/authorized_keys
```
or by editing the file `sudo nano ~/.ssh/authorized_keys` and copy/pasting the key in. It is perfectly acceptable to have multiple entries in the authorized_keys file, so SSH can support multiple clients.











