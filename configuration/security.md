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

A `key` is a 128bit or more encrypted public key. 






