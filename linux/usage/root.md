# Root user/sudo

The Linux operating system is a multi-user operating system which allows multiple users to log in and use the computer. To protect the computer (and the privacy of other users), the users' abilities are restricted. 

Most users are allowed to run most programs, and to save and edit files stored in their own home folder. Normal users are not normally allowed to edit files in other users' folders or any of the system files. There's a special user in Linux known as the **superuser**, which is usually given the username `root`. The superuser has unrestricted access to the computer and can do almost anything.

## sudo

You won't normally log into the computer as `root`, but you can use the `sudo` command to provide access as the superuser. If you log into your Raspberry Pi as the `pi` user, then you're logging in as a normal user. You can run commands as the `root` user by using the `sudo` command before the program you want to run. 

For example, if you want to install additional software on Raspberry Pi OS then you normally use the `apt` tool. To update the list of available software, you need to prefix the `apt` command with sudo:

`sudo apt update`

Find out more about the [apt commands](../software/apt.md).

You can also run a superuser shell by using `sudo su`. When running commands as a superuser there's nothing to protect against mistakes that could damage the system. It's recommended that you only run commands as the superuser when required, and to exit a superuser shell when it's no longer needed.

## Who can use sudo?

It would defeat the point of the security if anyone could just put `sudo` in front of their commands, so only approved users can use `sudo` to gain administrator privileges. The `pi` user is included in the `sudoers` file of approved users. To allow other users to act as a superuser, add the user to the `sudo` group with `usermod`.

[Find out more about users](users.md).
