# Root User / Sudo

The Linux operating system is a multi-user operating system which allows multiple users to login and use the computer. To protect the computer (and privacy of other users), users are restricted in what they can do. 

Most users are allowed to run most programs, and to save and edit files stored in their own home folder. Normal users are not normally allowed to edit files in other users folders or any of the system files. There is a special user in Linux known as the **superuser**, which is usually given the username `root`. The superuser has unrestricted access to the computer and can do almost anything.

## Sudo

You will not normally log into to the computer as root, but can instead use the sudo command to provide access as the superuser. If you log into your Raspberry Pi as the `pi` user then you are logging in as a normal user. You can run commands as the root user by using the `sudo` command before the program you want to run. 

For example if you want to install additional software on Raspbian then you normally use the `apt-get` tool. To be able to update the list of available software then you need to prefix the `apt-get` command command with sudo.
`sudo apt-get update`

Find out more about the [apt commands](../software/apt.md)

You can also run a superuser shell by using `sudo su`. When running commands as a superuser there is nothing to protect against mistakes that could damage the system. It is like disabling the safety guards on a machine. It makes it easier to access the insides, but the risk of damage is far greater. It is recommended that you only run commands as the superuser when required and to exit a superuser shell when it is no longer needed.

## Who can use Sudo?

It would defeat the point of the security if anyone could just put sudo in front of their commands, so only approved users can use sudo to gain administrator privileges. The `pi` user is included in the sudoers file. To allow other users to act as a superuser then you could add the user to the `sudo` group or add them using `visudo`.

[Find out more about users](users.md)
