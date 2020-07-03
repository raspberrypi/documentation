# Linux users

User management in Raspberry Pi OS is done on the command line. The default user is `pi`, and the password is `raspberry`. You can add users and change each user's password.

## Change your password

Once you're logged in as the `pi` user, it is highly advisable to use the `passwd` command to change the default password to improve your Pi's security.

Enter `passwd` on the command line and press `Enter`. You'll be prompted to enter your current password to authenticate, and then asked for a new password. Press `Enter` on completion and you'll be asked to confirm it. Note that no characters will be displayed while entering your password. Once you've correctly confirmed your password, you'll be shown a success message (`passwd: password updated successfully`), and the new password will apply immediately.

If your user has `sudo` permissions, you can change another user's password with `passwd` followed by the user's username. For example, `sudo passwd bob` will allow you to set the user `bob`'s password, and then some additional optional values for the user such as their name. Just press `Enter` to skip each of these options.

### Remove a user's password

You can remove the password for the user `bob` with `sudo passwd bob -d`.

## Create a new user

You can create additional users on your Raspberry Pi OS installation with the `adduser` command.

Enter `sudo adduser bob` and you'll be prompted for a password for the new user `bob`. Leave this blank if you don't want a password.

### Home folder

When you create a new user, they will have a home folder in `/home/`. The `pi` user's home folder is at `/home/pi/`.

#### skel

Upon creating a new user, the contents of `/etc/skel/` will be copied to the new user's home folder. You can add or modify dot-files such as the `.bashrc` in `/etc/skel/` to your requirements, and this version will be applied to new users.

## Sudoers

The default `pi` user on Raspberry Pi OS is a member of the `sudo` group. This gives the ability to run commands as root when preceded by `sudo`, and to switch to the root user with `sudo su`.

To add a new user to the `sudo` group, use the `adduser` command:

```bash
sudo adduser bob sudo
```

Note that the user `bob` will be prompted to enter their password when they run `sudo`. This differs from the behaviour of the `pi` user, since `pi` is not prompted for their password. If you wish to remove the password prompt from the new user, create a custom sudoers file and place it in the `/etc/sudoers.d` directory.

1. Create the file using `sudo visudo /etc/sudoers.d/010_bob-nopasswd`.
1. Insert the following contents on a single line: `bob ALL=(ALL) NOPASSWD: ALL`
1. Save the file and exit.

Once you have exited the editor, the file will be checked for any syntax errors. If no errors were detected, the file will be saved and you will be returned to the shell prompt. If errors were detected, you will be asked 'what now?' Press the 'enter' key on your keyboard: this will bring up a list of options. You will probably want to use 'e' for '(e)dit sudoers file again,' so you can edit the file and fix the problem. **Note that choosing option 'Q' will save the file with any syntax errors still in place, which makes it impossible for _any_ user to use the sudo command.**

Note that it is standard practice on Linux to have the user prompted for their password when they run `sudo`, since it makes the system slightly more secure.

## Delete a user

You can delete a user on your system with the command `userdel`. Apply the `-r` flag to remove their home folder too:

```bash
sudo userdel -r bob
```
