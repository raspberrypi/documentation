# Linux users

User management in Raspbian is done on the command line. The default user is `pi` with the password `raspberry`. You can add users and change each user's password.

## Change your password

When logged in as the `pi` user you can change your password with the `passwd` command.

Enter `passwd` on the command line and hit `Enter`. You'll be prompted to enter your current password to authenticate, and then asked for a new password. Hit `Enter` on completion and you'll be asked to confirm it. Note that no characters will be displayed while entering your password. Once you've correctly confirmed, you'll be shown a success message (`passwd: password updated successfully`) and the new password will be in effect immediately.

If your user has sudo permissions, you can change another user's password with `passwd` proceeded by the user's username, e.g. `sudo passwd bob` will allow you to set the user `bob`'s password, and then some additional optional values for the user such as their name. Just hit `Enter` to skip each of these options.

### Remove a user's password

You can remove the password for the user `bob` with `sudo passwd bob -d`.

## Create a new user

You can create additional users on your Raspbian installation with the `adduser` command.

Enter `sudo adduser bob` and you'll be prompted for a password for the new user `bob`. Leave blank for no password.

### Home folder

When you create a new user, they will have a home folder in `/home/`. The `pi` user's home folder is at `/home/pi/`.

#### skel

Upon creating a new user, the contents of `/etc/skel/` will be copied to the new user's home folder. You can add or modify dotfiles such as the `.bashrc` in `/etc/skel/` to your taste and this version will be applied to new users created.

## Sudoers

The default `pi` user on Raspbian is a sudoer. This gives the ability to run commands as root when preceded by `sudo`, and to switch to the root user with `sudo su`.

To add a new user to sudoers, type `sudo visudo` (from a sudoer user) and find the line `root    ALL=(ALL:ALL) ALL`, found under the commented header '# User privilege specification'. Copy this line and switch from `root` to the username. To allow passwordless root access, change to `NOPASSWD: ALL`. The example below gives the user `bob` passwordless sudo access:

```bash
# User privilege specification
root  ALL=(ALL:ALL) ALL
bob   ALL = NOPASSWD: ALL
```

Save and exit to apply the changes. **Be careful**. It is possible to remove your own sudo rights by accident.

Note you can change the editor the `visudo` command uses (the default is Nano) by entering:

```bash
update-alternatives --set editor /usr/bin/vim.tiny
```

This sets the editor to Vim.

## Delete a user

You can delete a user on your system with the command `userdel`. Apply the `-r` flag to remove their home folder too:

```bash
sudo userdel -r bob
```
